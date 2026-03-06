"""
API Views for Vajebaat Management.

Permission model:
- Members: Admin only (read + create)
- Forms (Takhmeen): Admin can list/read; anyone can POST (no auth needed for submission)
- Appointments: Admin can list/read/update_status/assign_slot; anyone can POST (public booking)
- Dates: Admin CRUD
- Slots: Admin read-only (filterable by date)
- Dashboard Stats: Admin only
"""

from django.db import transaction
from django.db.models import Q, Count, Sum, F, Value
from django.db.models.functions import Greatest
from django.utils import timezone
from django.http import HttpResponse

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes as perm_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import (
    VajebaatMember, VajebaatForm, VajebaatAppointment,
    VajebaatDate, VajebaatSlot,
)
from .serializers import (
    VajebaatMemberSerializer,
    PublicMemberSerializer,
    VajebaatFormSerializer,
    VajebaatAppointmentSerializer,
    VajebaatAppointmentStatusSerializer,
    VajebaatDateSerializer,
    VajebaatSlotSerializer,
    AssignSlotSerializer,
    MembersDirectorySerializer,
    PublicAppointmentStatusSerializer,
)
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import PageNumberPagination


import logging
logger = logging.getLogger(__name__)


# ============================================================
# Existing ViewSets (unchanged logic)
# ============================================================

class VajebaatMemberViewSet(viewsets.ModelViewSet):
    """
    Vajebaat member directory — Admin only.
    GET  /api/vajebaat/members/           — List all members
    GET  /api/vajebaat/members/{id}/      — Get member details
    GET  /api/vajebaat/members/by_its/    — Lookup by ITS number (?its=12345678)
    POST /api/vajebaat/members/           — Create member (admin)
    """
    queryset = VajebaatMember.objects.all()
    serializer_class = VajebaatMemberSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(its_number__icontains=search) |
                Q(name__icontains=search) |
                Q(mohalla__icontains=search)
            )
        return qs

    @action(detail=False, methods=['get'], url_path='by_its',
            permission_classes=[AllowAny])
    def by_its(self, request):
        """
        Public endpoint: restricted member lookup by ITS number.
        Returns only name + masked ITS. No sensitive data exposed.
        GET /api/vajebaat/members/by_its/?its=12345678
        """
        its = request.query_params.get('its', '').strip()
        if not its:
            return Response(
                {'detail': 'ITS number is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            member = VajebaatMember.objects.get(its_number=its)
        except VajebaatMember.DoesNotExist:
            return Response(
                {'detail': 'No member found for this ITS number.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PublicMemberSerializer(member)
        return Response(serializer.data)


class VajebaatFormViewSet(viewsets.ModelViewSet):
    """
    Vajebaat Takhmeen form records.
    GET  /api/vajebaat/forms/        — List all forms (Admin only)
    GET  /api/vajebaat/forms/{id}/   — Get form (Admin only)
    POST /api/vajebaat/forms/        — Create form (public — no auth required)
    """
    queryset = VajebaatForm.objects.all()
    serializer_class = VajebaatFormSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]

    def get_throttles(self):
        if self.action == 'create':
            return [AnonRateThrottle()]
        return []


# ============================================================
# UPDATED: Appointment ViewSet with assign_slot
# ============================================================

class VajebaatAppointmentViewSet(viewsets.ModelViewSet):
    """
    Vajebaat appointment bookings.
    GET   /api/vajebaat/appointments/                       — List (Admin only)
    GET   /api/vajebaat/appointments/{id}/                  — Retrieve (Admin only)
    POST  /api/vajebaat/appointments/                       — Book appointment (public)
    PATCH /api/vajebaat/appointments/{id}/update_status/    — Update status (Admin only)
    POST  /api/vajebaat/appointments/{id}/assign-slot/      — Assign slot (Admin only)
    PATCH /api/vajebaat/appointments/{id}/reschedule/       — Reschedule slot (Admin only)
    PATCH /api/vajebaat/appointments/{id}/cancel/           — Cancel appointment (Admin only)
    GET   /api/vajebaat/appointments/check_status/          — Public status check (?its=X)
    """
    queryset = VajebaatAppointment.objects.select_related('slot', 'slot__date').all()
    serializer_class = VajebaatAppointmentSerializer
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter.upper())
        return qs

    def get_permissions(self):
        if self.action in ('create', 'check_status'):
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]

    def get_throttles(self):
        if self.action == 'create':
            return [AnonRateThrottle()]
        return []

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Public booking endpoint: Allows booking without requiring Member record.
        Handles both 'its_number'/'preferred_date'/'slot' and 'its'/'date'/'slot_id'.
        """
        data = request.data.copy()
        if 'its' in data and 'its_number' not in data:
            data['its_number'] = data['its']
        if 'date' in data and 'preferred_date' not in data:
            data['preferred_date'] = data['date']
        if 'slot_id' in data and 'slot' not in data:
            data['slot'] = data['slot_id']

        its_number = str(data.get('its_number', '')).strip()
        if not its_number:
            return Response(
                {'its_number': 'This field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Lookup member silently (don't block if not found)
        member = VajebaatMember.objects.filter(its_number=its_number).first()

        # Capacity check if slot is provided
        slot_id = data.get('slot')
        if slot_id:
            try:
                slot = VajebaatSlot.objects.select_for_update().get(pk=slot_id)
                confirmed_count = slot.appointments.filter(status='CONFIRMED').count()
                if confirmed_count >= slot.capacity:
                    return Response(
                        {'slot': 'This slot is full. Please pick another.'},
                        status=status.HTTP_409_CONFLICT
                    )
            except VajebaatSlot.DoesNotExist:
                return Response({'slot': 'Slot not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save(member=member)

        # Auto-confirm if slot was selected
        if appointment.slot:
            appointment.status = 'CONFIRMED'
            appointment.confirmed_at = timezone.now()
            appointment.save(update_fields=['status', 'confirmed_at'])
            
            # Trigger confirmation notification
            from .tasks import send_slot_confirmed_notification_task
            transaction.on_commit(lambda: send_slot_confirmed_notification_task.delay(appointment.id, appointment.slot.id))
        else:
            # Request received notification
            from .tasks import send_appointment_confirmation_task
            transaction.on_commit(lambda: send_appointment_confirmation_task.delay(appointment.id))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, member=None):
        """Save appointment, prioritizing user-submitted data over member record."""
        logger.info("[Vajebaat] perform_create starting...")
        
        # Save directly what was submitted. 
        # If member exists, we link it. If email is not provided, we fallback to member email.
        email = serializer.validated_data.get('email', '')
        if not email and member and member.email:
            email = member.email
            logger.info(f"[Vajebaat] No email submitted, falling back to member email: {email}")

        appointment = serializer.save(
            member=member,
            mobile=serializer.validated_data.get('mobile', ''),
            email=email
        )
        
        logger.info(f"[Vajebaat] Appointment {appointment.id} saved. Member Linked: {member.its_number if member else 'None'}, Email: {appointment.email}")

        def _post_create():
            logger.info(f"[Vajebaat] Dispatching background tasks for Appointment {appointment.id}")
            from .tasks import send_appointment_confirmation_task
            send_appointment_confirmation_task.delay(appointment.id)
            self._trigger_sheets_sync()

        transaction.on_commit(_post_create)

    # ----------------------------------------------------------
    # Update Status (generic)
    # ----------------------------------------------------------

    @action(detail=True, methods=['patch'], url_path='update_status',
            permission_classes=[IsAuthenticated, IsAdminUser])
    def update_status(self, request, pk=None):
        """
        PATCH /api/vajebaat/appointments/{id}/update_status/
        Body: { "status": "CONFIRMED" }
        """
        appointment = self.get_object()
        serializer = VajebaatAppointmentStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appointment.status = serializer.validated_data['status']
        appointment.save(update_fields=['status'])

        transaction.on_commit(lambda: self._trigger_sheets_sync())

        return Response(
            VajebaatAppointmentSerializer(appointment).data,
            status=status.HTTP_200_OK
        )

    # ----------------------------------------------------------
    # Assign Slot
    # ----------------------------------------------------------

    @action(detail=True, methods=['post'], url_path='assign-slot',
            permission_classes=[IsAuthenticated, IsAdminUser])
    def assign_slot(self, request, pk=None):
        """
        POST /api/vajebaat/appointments/{id}/assign-slot/
        Body: { "slot_id": 1 }
        Uses transaction.atomic() + select_for_update() for race-condition safety.
        """
        appointment = self.get_object()

        serializer = AssignSlotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        slot_id = serializer.validated_data['slot_id']

        try:
            with transaction.atomic():
                slot = VajebaatSlot.objects.select_for_update().get(pk=slot_id)

                confirmed_count = slot.appointments.filter(
                    status='CONFIRMED'
                ).count()

                if confirmed_count >= slot.capacity:
                    return Response(
                        {'detail': 'This slot is full. Please choose another.'},
                        status=status.HTTP_409_CONFLICT
                    )

                appointment.slot = slot
                appointment.status = 'CONFIRMED'
                appointment.confirmed_at = timezone.now()
                appointment.save(
                    update_fields=['slot', 'status', 'confirmed_at']
                )

        except VajebaatSlot.DoesNotExist:
            return Response(
                {'detail': 'Slot not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Notifications AFTER successful commit (via Celery)
        def _post_assign():
            from .tasks import send_slot_confirmed_notification_task
            send_slot_confirmed_notification_task.delay(appointment.id, slot.id)
            self._trigger_sheets_sync()

        transaction.on_commit(_post_assign)

        return Response(
            VajebaatAppointmentSerializer(appointment).data,
            status=status.HTTP_200_OK
        )

    # ----------------------------------------------------------
    # Reschedule Slot
    # ----------------------------------------------------------

    @action(detail=True, methods=['patch'], url_path='reschedule',
            permission_classes=[IsAuthenticated, IsAdminUser])
    def reschedule(self, request, pk=None):
        """
        PATCH /api/vajebaat/appointments/{id}/reschedule/
        Body: { "slot_id": 5 }
        Moves an appointment to a different slot with capacity check.
        """
        appointment = self.get_object()

        serializer = AssignSlotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_slot_id = serializer.validated_data['slot_id']

        if appointment.slot and appointment.slot.id == new_slot_id:
            return Response(
                {'detail': 'Same slot selected. No changes made.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                new_slot = VajebaatSlot.objects.select_for_update().get(pk=new_slot_id)

                confirmed_count = new_slot.appointments.filter(
                    status='CONFIRMED'
                ).count()

                if confirmed_count >= new_slot.capacity:
                    return Response(
                        {'detail': 'Target slot is full. Please choose another.'},
                        status=status.HTTP_409_CONFLICT
                    )

                appointment.slot = new_slot
                appointment.status = 'RESCHEDULED'
                appointment.confirmed_at = timezone.now()
                appointment.save(update_fields=['slot', 'status', 'confirmed_at'])

        except VajebaatSlot.DoesNotExist:
            return Response(
                {'detail': 'Slot not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        def _post_reschedule():
            logger.info(f"[WhatsApp] Reschedule notification for appointment {appointment.id}")
            from .tasks import send_slot_rescheduled_notification_task
            send_slot_rescheduled_notification_task.delay(appointment.id, new_slot.id)
            self._trigger_sheets_sync()

        transaction.on_commit(_post_reschedule)

        return Response(
            VajebaatAppointmentSerializer(appointment).data,
            status=status.HTTP_200_OK
        )

    # ----------------------------------------------------------
    # Cancel Appointment
    # ----------------------------------------------------------

    @action(detail=True, methods=['patch'], url_path='cancel',
            permission_classes=[IsAuthenticated, IsAdminUser])
    def cancel(self, request, pk=None):
        """
        PATCH /api/vajebaat/appointments/{id}/cancel/
        Sets status=CANCELLED, releases the slot.
        """
        appointment = self.get_object()

        if appointment.status == 'CANCELLED':
            return Response(
                {'detail': 'Appointment is already cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        old_slot = appointment.slot  # capture before clearing

        with transaction.atomic():
            appointment.status = 'CANCELLED'
            appointment.slot = None
            appointment.save(update_fields=['status', 'slot'])

        def _post_cancel():
            logger.info(f"[WhatsApp] Cancel notification for appointment {appointment.id}")
            from .tasks import send_appointment_cancelled_notification_task
            send_appointment_cancelled_notification_task.delay(
                appointment.id, 
                old_slot.id if old_slot else None
            )
            self._trigger_sheets_sync()

        transaction.on_commit(_post_cancel)

        return Response(
            VajebaatAppointmentSerializer(appointment).data,
            status=status.HTTP_200_OK
        )

    # ----------------------------------------------------------
    # Public Status Check
    # ----------------------------------------------------------

    @action(detail=False, methods=['get'], url_path='check_status',
            permission_classes=[AllowAny])
    def check_status(self, request):
        """
        GET /api/vajebaat/appointments/check_status/?its=12345678
        Returns the status of the most recent appointment for the given ITS.
        """
        its = request.query_params.get('its', '').strip()
        if not its:
            return Response(
                {'detail': 'ITS number is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment = VajebaatAppointment.objects.filter(
            its_number=its
        ).select_related('slot', 'slot__date').order_by('-created_at').first()

        if not appointment:
            return Response(
                {'detail': 'No appointment record found for this ITS number.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PublicAppointmentStatusSerializer(appointment)
        return Response(serializer.data)

    # ----------------------------------------------------------
    # Helper: Google Sheets sync
    # ----------------------------------------------------------

    @staticmethod
    def _trigger_sheets_sync():
        """Auto-sync Vajebaat data to Google Sheets via Celery."""
        from .tasks import sync_vajebaat_to_sheets_task
        sync_vajebaat_to_sheets_task.delay()

# ============================================================
# NEW: Date & Slot ViewSets
# ============================================================

class VajebaatDateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Admin-only read access to Vajebaat appointment dates.
    GET    /api/vajebaat/dates/       — List all dates
    GET    /api/vajebaat/dates/{id}/  — Get date detail

    Write operations removed — dates are managed via Django admin or shell.
    """
    queryset = VajebaatDate.objects.filter(is_active=True).annotate(
        slot_count=Count('slots')
    )
    serializer_class = VajebaatDateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = None


class VajebaatSlotViewSet(viewsets.ModelViewSet):
    """
    Admin-only access to slots.
    GET    /api/vajebaat/slots/            — List all slots
    GET    /api/vajebaat/slots/?date_id=X  — Filter by date
    GET    /api/vajebaat/slots/{id}/       — Get slot detail
    PATCH  /api/vajebaat/slots/{id}/       — Update capacity/is_active (Admin)
    GET    /api/vajebaat/slots/{id}/users/ — List users booked in this slot (Admin)
    """
    serializer_class = VajebaatSlotSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = None

    def get_queryset(self):
        qs = VajebaatSlot.objects.select_related('date').annotate(
            confirmed_count=Count(
                'appointments',
                filter=Q(appointments__status='CONFIRMED')
            )
        )
        date_id = self.request.query_params.get('date_id')
        if date_id:
            qs = qs.filter(date_id=date_id)
        return qs

    @action(detail=True, methods=['get'], url_path='users',
            permission_classes=[IsAuthenticated, IsAdminUser])
    def users(self, request, pk=None):
        """
        GET /api/vajebaat/slots/{id}/users/
        Returns all appointments booked in this specific slot.
        """
        slot = self.get_object()
        appointments = slot.appointments.all().order_by('created_at')
        serializer = VajebaatAppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


# ============================================================
# NEW: Dashboard Stats endpoint
# ============================================================

@api_view(['GET'])
@perm_classes([IsAuthenticated, IsAdminUser])
def dashboard_stats(request):
    """
    GET /api/vajebaat/dashboard-stats/
    Returns aggregated metrics for the admin dashboard.
    Optimized: single combined query for appointment counts, SQL-level slot aggregation.
    """
    today = timezone.localdate()

    # Single query for all appointment aggregates
    apt_stats = VajebaatAppointment.objects.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='PENDING')),
        confirmed_today=Count(
            'id',
            filter=Q(status='CONFIRMED', confirmed_at__date=today)
        ),
    )

    # SQL-level available slot calculation
    slot_agg = VajebaatSlot.objects.filter(
        date__date=today,
        date__is_active=True
    ).annotate(
        confirmed_count=Count(
            'appointments',
            filter=Q(appointments__status='CONFIRMED')
        )
    ).aggregate(
        available=Sum(
            Greatest(F('capacity') - F('confirmed_count'), Value(0))
        )
    )

    return Response({
        'total_appointments': apt_stats['total'],
        'pending': apt_stats['pending'],
        'confirmed_today': apt_stats['confirmed_today'],
        'available_slots_today': slot_agg['available'] or 0,
    })


# ============================================================
# Members Directory endpoint (flat appointment-based view)
# ============================================================

class DirectoryPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


@api_view(['GET'])
@perm_classes([IsAuthenticated, IsAdminUser])
def members_directory(request):
    """
    GET /api/vajebaat/members-directory/
    Paginated, filterable directory of all appointment applicants.
    ?status=CONFIRMED  — filter by status
    ?search=6045       — search ITS or name
    """
    qs = (
        VajebaatAppointment.objects
        .select_related('slot', 'slot__date')
        .order_by('-created_at')
    )

    # Status filter
    status_filter = request.query_params.get('status', '').strip().upper()
    if status_filter in ('PENDING', 'CONFIRMED', 'COMPLETED', 'CANCELLED'):
        qs = qs.filter(status=status_filter)

    # Search filter
    search = request.query_params.get('search', '').strip()
    if search:
        qs = qs.filter(
            Q(its_number__icontains=search) |
            Q(name__icontains=search) |
            Q(mobile__icontains=search)
        )

    paginator = DirectoryPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = MembersDirectorySerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


# ============================================================
# Google Sheets Sync endpoint
# ============================================================

@api_view(['POST'])
@perm_classes([IsAuthenticated, IsAdminUser])
def sync_vajebaat_sheet(request):
    """
    POST /api/vajebaat/sync-sheet/
    Manually trigger full sync of Vajebaat data to Google Sheets.
    """
    from .google_sheets import sync_vajebaat_members

    success, detail = sync_vajebaat_members()
    if success:
        return Response({
            'status': 'success',
            'records_synced': detail,
        })
    return Response(
        {'status': 'error', 'detail': str(detail)},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


# ============================================================
# CSV Export endpoint
# ============================================================

@api_view(['GET'])
@perm_classes([IsAuthenticated, IsAdminUser])
def export_csv(request):
    """
    GET /api/vajebaat/export-csv/
    Download all Vajebaat appointment data as a CSV file.
    """
    import csv

    appointments = (
        VajebaatAppointment.objects
        .select_related('slot', 'slot__date')
        .order_by('-created_at')
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vajebaat_members.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ITS', 'Name', 'Mobile', 'Preferred Date',
        'Assigned Date', 'Slot Time', 'Status',
        'Confirmed At', 'Created At',
    ])

    for apt in appointments:
        assigned_date = ''
        slot_time = ''
        if apt.slot:
            if apt.slot.date:
                assigned_date = str(apt.slot.date.date)
            slot_time = (
                f"{apt.slot.start_time.strftime('%H:%M')} – "
                f"{apt.slot.end_time.strftime('%H:%M')}"
            )

        writer.writerow([
            apt.its_number,
            apt.name,
            apt.mobile or '',
            str(apt.preferred_date) if apt.preferred_date else '',
            assigned_date,
            slot_time,
            apt.status,
            apt.confirmed_at.strftime('%Y-%m-%d %H:%M') if apt.confirmed_at else '',
            apt.created_at.strftime('%Y-%m-%d %H:%M') if apt.created_at else '',
        ])

    return response


@api_view(['GET'])
@perm_classes([IsAuthenticated, IsAdminUser])
def export_pdf(request, pk=None):
    """
    GET /api/vajebaat/appointments/{id}/export-pdf/
    Placeholder for PDF generation. Returns a simple text response for now.
    """
    try:
        from .models import VajebaatAppointment
        apt = VajebaatAppointment.objects.get(pk=pk)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="vajebaat_{apt.its_number}.pdf"'
        response.write(f"PDF Export for Appointment {apt.id}\nITS: {apt.its_number}\nName: {apt.name}")
        return response
    except Exception as e:
        return Response({'detail': str(e)}, status=404)


# ============================================================
# Public: Available Slots endpoint
# ============================================================

@api_view(['GET'])
@perm_classes([AllowAny])
def available_slots(request):
    """
    GET /api/vajebaat/available-slots/?date=YYYY-MM-DD
    Returns a simple list of slots with availability status for the public booking page.
    Efficiently filters for active dates/slots and checks capacity.
    """
    date_str = request.query_params.get('date')
    if not date_str:
        return Response(
            {'detail': 'Date is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    slots = VajebaatSlot.objects.filter(
        date__date=date_str,
        date__is_active=True,
        is_active=True
    ).annotate(
        confirmed_count=Count(
            'appointments',
            filter=Q(appointments__status='CONFIRMED')
        )
    ).order_by('slot_number')

    results = []
    for s in slots:
        if s.confirmed_count < s.capacity:
            results.append({
                'id': s.id,
                'slot': f"{s.start_time.strftime('%H:%M')} – {s.end_time.strftime('%H:%M')}",
                'available': True
            })

    return Response(results)
