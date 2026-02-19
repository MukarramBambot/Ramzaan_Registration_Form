"""
API Views for Azaan & Takhbira Duty Management System.
Handles registration, duty assignment, unlocking, and reminders.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.db.models import Prefetch
from django.utils import timezone
import logging

from .models import (
    Registration, AuditionFile, DutyAssignment, 
    UnlockLog, Reminder, ReminderLog, KhidmatRequest, RegistrationCorrection
)
from .serializers import (
    RegistrationSerializer, RegistrationCreateSerializer,
    AuditionFileSerializer, DutyAssignmentSerializer,
    DutyAssignmentCreateSerializer, UnlockSerializer,
    UnlockLogSerializer, ReminderSerializer, ReminderLogSerializer,
    KhidmatRequestSerializer, RegistrationCorrectionSerializer
)
from .utils import (
    create_reminder_for_assignment, cancel_reminders_for_assignment,
    safe_task_delay, get_reporting_time
)
from .tasks import sync_to_sheets_task
from .tasks import send_registration_confirmation_task
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class HealthCheckView(APIView):
    """
    Health check endpoint for production monitoring.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok", "timestamp": timezone.now()}, status=status.HTTP_200_OK)

logger = logging.getLogger(__name__)




class MeView(APIView):
    """Return current authenticated user info."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'id': user.id,
        })


class RegistrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user registrations.
    """
    queryset = Registration.objects.all().prefetch_related('audition_files', 'duty_assignments')
    parser_classes = (MultiPartParser, FormParser)
    pagination_class = None  # Frontend sidebar/dashboard expects full list
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'search':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RegistrationCreateSerializer
        return RegistrationSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create new registration.
        Minimized sync work: DB save + initial metadata.
        Heavy lifting (Notifications, Sheets) moved to Celery via on_commit.
        """
        try:
            # 1. Fast Validation
            its_number = request.data.get('its_number')
            if its_number and Registration.objects.filter(its_number=its_number).exists():
                return Response(
                    {'its_number': ['ITS Number already registered.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Serializer Validation & Save
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            registration = serializer.save()
            
            # 3. Handle Files (Sync Save but minimal meta)
            files = request.FILES.getlist('audition_files') or request.FILES.getlist('media_files')
            
            # Validation: Max 6 files
            if files and len(files) > 6:
                transaction.set_rollback(True)
                return Response(
                    {'error': 'Maximum 6 audition files allowed'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validation & Saving Loop
            for f in files:
                # Max 15MB (15 * 1024 * 1024 bytes)
                if f.size > 15 * 1024 * 1024:
                    transaction.set_rollback(True)
                    return Response(
                        {'error': f'File {f.name} exceeds 15MB limit.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Use .create() instead of bulk_create to ensure file storage works
                AuditionFile.objects.create(registration=registration, audition_file_path=f)

            # 4. Schedule Background Tasks
            def schedule_registration_tasks():
                logger.info(f"Offloading post-registration tasks for ID: {registration.id}")
                safe_task_delay(send_registration_confirmation_task, registration.id, non_blocking=True)
                safe_task_delay(sync_to_sheets_task, registration.id, non_blocking=True)

            transaction.on_commit(schedule_registration_tasks)

            # 5. Return Minimal Success Immediately
            return Response({
                'id': registration.id,
                'status': 'success',
                'message': 'Registration received'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"REGISTRATION_FAILURE: {str(e)}", exc_info=True)
            # Ensure rollback happens on any unexpected error
            transaction.set_rollback(True) 
            return Response(
                {'error': 'Registration failed. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def auditions(self, request, pk=None):
        """
        Returns all audition files for a specific registration.
        """
        registration = self.get_object()
        auditions = registration.audition_files.all().order_by('-uploaded_at')
        serializer = AuditionFileSerializer(auditions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search for registration and its assignments by ITS number"""
        its_number = request.query_params.get('its')
        logger.info(f"API: Search initiated for ITS {its_number}")
        if not its_number:
            return Response(
                {'error': 'ITS number is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Optimize with prefetch for duties and their pending requests
            registration = Registration.objects.prefetch_related(
                Prefetch(
                    'duty_assignments',
                    queryset=DutyAssignment.objects.all().prefetch_related(
                        Prefetch(
                            'requests',
                            queryset=KhidmatRequest.objects.filter(status='pending'),
                            to_attr='pending_requests'
                        )
                    )
                ),
                'audition_files'
            ).get(its_number=its_number)
            
            assignments = registration.duty_assignments.all()
            
            # Map duties as per requested format
            duties = []
            for duty in assignments:
                display_name = duty.get_namaaz_type_display()
                # Split "Fajar Azaan" into ["Fajar", "Azaan"]
                parts = display_name.split(' ')
                namaaz = parts[0] if len(parts) > 0 else display_name
                duty_type = parts[1] if len(parts) > 1 else ""
                
                # Check for pending requests
                pending_request = getattr(duty, 'pending_requests', [])
                request_status = pending_request[0].status if pending_request else None
                request_type = pending_request[0].request_type if pending_request else None
                
                duties.append({
                    "id": duty.id,
                    "date": duty.duty_date.strftime('%d/%m/%Y'),
                    "namaaz": namaaz,
                    "type": duty_type,
                    "request_status": request_status,
                    "request_type": request_type,
                    "reporting_time": get_reporting_time(duty)
                })
            
            # Map audition files
            audition_files = []
            for file in registration.audition_files.all():
                url = file.audition_file_path.url if file.audition_file_path else ""
                # Ensure full URL for absolute paths
                if url and not url.startswith('http'):
                    url = request.build_absolute_uri(url)
                
                audition_files.append({
                    "id": file.id,
                    "url": url,
                    "type": file.audition_file_type,
                    "name": file.audition_display_name
                })

            return Response({
                "full_name": registration.full_name,
                "its_number": registration.its_number,
                "register_for": registration.get_preference_display(),
                "status": registration.status,
                "duties": duties,
                "audition_files": audition_files
            })
            
        except Registration.DoesNotExist:
            return Response(
                {'error': 'No registration found for this ITS number'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def sync_to_sheets(self, request):
        """Trigger manual bulk sync to Google Sheets."""
        from .google_sheets import sync_all_to_sheets
        logger.info(f"API: Manual Google Sheets sync triggered by {request.user.username}")
        
        success, result = sync_all_to_sheets()
        if success:
            if result == 0:
                return Response({'message': 'Sync successful (Headers only). No registration records found in database.'})
            return Response({'message': f'Successfully synced {result} registrations to Google Sheets.'})
        else:
            return Response(
                {'error': f'Failed to sync to Google Sheets: {result}. Check server logs for details.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AuditionFileViewSet(viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin, viewsets.mixins.UpdateModelMixin):
    queryset = AuditionFile.objects.all()
    serializer_class = AuditionFileSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['patch'])
    def select_audition(self, request, pk=None):
        """
        Selects a specific audition file for a registration.
        Ensures only one file is selected per registration.
        """
        audition = self.get_object()
        registration = audition.registration
        
        try:
            with transaction.atomic():
                # Deselect all others for this registration
                registration.audition_files.update(is_selected=False)
                
                # Select the target
                audition.is_selected = True
                audition.save(update_fields=['is_selected'])
                
            return Response({'status': 'success', 'message': 'Audition selected'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def audition_files(self, request, pk=None):
        """Get audition files for a specific registration"""
        registration = self.get_object()
        files = registration.audition_files.all()
        serializer = AuditionFileSerializer(files, many=True)
        return Response(serializer.data)


class DutyAssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for duty roster management.
    
    list: Get all duty assignments (Excel-style grid data)
    retrieve: Get single duty assignment
    create: Assign duty to user (auto-locks and creates reminder)
    update/patch: Not allowed (must unlock first)
    destroy: Delete assignment (cancels reminder)
    """
    queryset = DutyAssignment.objects.all().select_related('assigned_user')
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = None  # Grid view expects full data
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DutyAssignmentCreateSerializer
        return DutyAssignmentSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create new duty assignment.
        Automatically locks and creates reminder.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get validated data
        duty_date = serializer.validated_data['duty_date']
        namaaz_type = serializer.validated_data['namaaz_type']
        user_id = serializer.validated_data['assigned_user_id']
        
        # Create assignment (locked by default)
        assignment = DutyAssignment.objects.create(
            duty_date=duty_date,
            namaaz_type=namaaz_type,
            assigned_user_id=user_id,
            locked=True
        )
        
        # Update registration status to ALLOTTED
        registration = Registration.objects.get(id=user_id)
        if registration.status != 'ALLOTTED':
            registration.status = 'ALLOTTED'
            registration.save(update_fields=['status'])
            logger.info(f"Updated registration {registration.id} status to ALLOTTED")
        
        # Create automatic reminder
        reminder = create_reminder_for_assignment(assignment)
        
        logger.info(f"Duty assigned: {assignment}, Reminder: {reminder.id if reminder else 'FAILED'}")
        
        # Return assignment data
        output_serializer = DutyAssignmentSerializer(assignment)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Prevent direct updates - must unlock first"""
        assignment = self.get_object()
        
        if assignment.locked:
            return Response(
                {
                    'error': 'This duty is locked. Use emergency unlock to make changes.',
                    'locked_at': assignment.locked_at
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """Delete assignment and cancel reminder"""
        assignment = self.get_object()
        
        # Cancel reminders
        cancel_reminders_for_assignment(assignment)
        
        logger.info(f"Duty assignment deleted: {assignment}")
        
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'], url_path='unassign-khidmat')
    @transaction.atomic
    def unassign_khidmat(self, request):
        """
        Refactored: Unassign a user from a khidmat slot.
        - Removes assigned_user link
        - Sets locked = False
        - Updates Registration.status back to APPROVED
        - Logs action in UnlockLog and audit fields
        """
        khidmat_id = request.data.get('khidmat_id')
        if not khidmat_id:
            return Response({'error': 'khidmat_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Use select_for_update to handle concurrency
            assignment = DutyAssignment.objects.select_for_update().get(pk=khidmat_id)
        except DutyAssignment.DoesNotExist:
            return Response({'error': 'Duty assignment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Reason is no longer required - using default for audit tracking
        reason = "Unassigned via Admin Dashboard"
        
        assigned_user = assignment.assigned_user
        if not assigned_user:
            return Response({'error': 'No user assigned to this slot'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Update Registration status back to APPROVED
        # This allows the user to be re-allotted later if needed
        assigned_user.status = 'APPROVED'
        assigned_user.save(update_fields=['status'])
        
        # 2. Log exactly what happened (Legacy Log for audit history)
        UnlockLog.objects.create(
            duty_assignment=assignment,
            reason=reason,
            unlocked_by=request.user.username if request.user.is_authenticated else "Admin",
            duty_date=assignment.duty_date,
            namaaz_type=assignment.namaaz_type,
            original_user_name=assigned_user.full_name,
            original_user_its=assigned_user.its_number
        )
        
        # 3. Update Audit fields and clear assignment in DutyAssignment
        assignment.assigned_user = None
        assignment.locked = False
        assignment.removed_by = request.user if request.user.is_authenticated else None
        assignment.removed_at = timezone.now()
        assignment.removal_reason = reason
        assignment.save()
        
        # 4. Cancel existing reminders
        cancel_reminders_for_assignment(assignment)
        
        logger.info(f"UNASSIGN_SUCCESS: Khidmat {khidmat_id} unassigned from {assigned_user.its_number} by {request.user}")
        
        return Response({'success': True})
    
    @action(detail=False, methods=['get'])
    def grid(self, request):
        """
        Get roster data in Excel-style grid format.
        Returns data organized by date and namaaz type.
        """
        assignments = self.get_queryset()
        
        # Organize by date
        grid_data = {}
        for assignment in assignments:
            date_key = assignment.duty_date.isoformat()
            
            if date_key not in grid_data:
                grid_data[date_key] = {}
            
            user = assignment.assigned_user
            grid_data[date_key][assignment.namaaz_type] = {
                'id': assignment.id,
                'user_id': user.id if user else None,
                'user_name': user.full_name if user else None,
                'user_its': user.its_number if user else None,
                'user_email': user.email if user else None,
                'user_phone': user.phone_number if user else None,
                'locked': assignment.locked,
                'locked_at': assignment.locked_at
            }
        
        return Response(grid_data)


class UnlockLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing unlock audit logs.
    Read-only for transparency and auditing.
    """
    queryset = UnlockLog.objects.all()
    serializer_class = UnlockLogSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ReminderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing reminders.
    Read-only - reminders are created/updated automatically.
    """
    queryset = Reminder.objects.all().select_related('duty_assignment', 'duty_assignment__assigned_user')
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending reminders"""
        pending = self.queryset.filter(status='PENDING')
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get reminders scheduled for next 7 days"""
        from datetime import timedelta
        
        now = timezone.now()
        week_later = now + timedelta(days=7)
        
        upcoming = self.queryset.filter(
            status='PENDING',
            scheduled_datetime__gte=now,
            scheduled_datetime__lte=week_later
        )
        
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)


class ReminderLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing reminder logs.
    For debugging and monitoring.
    """
    queryset = ReminderLog.objects.all().select_related('reminder')
    serializer_class = ReminderLogSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class KhidmatRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Khidmat (duty) cancellation and reallocation requests.
    
    Endpoints:
    - POST /api/khidmat-requests/ - Create new request (user)
    - GET /api/khidmat-requests/?status=pending - List requests (admin)
    - POST /api/khidmat-requests/{id}/approve/ - Approve request (admin)
    - POST /api/khidmat-requests/{id}/reject/ - Reject request (admin)
    """
    queryset = KhidmatRequest.objects.all().select_related(
        'assignment',
        'assignment__assigned_user'
    ).order_by('-created_at')
    serializer_class = KhidmatRequestSerializer
    
    def get_permissions(self):
        """
        Allow unauthenticated users to create requests.
        Require admin authentication for approve/reject.
        """
        if self.action in ['create']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    
    def get_queryset(self):
        """
        Filter by status if provided in query params.
        Example: /api/khidmat-requests/?status=pending
        """
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Create a new khidmat request.
        Validates that user has active duty assignment.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        khidmat_request_id = serializer.data['id']
        
        # Trigger Notification (WhatsApp + Email) via Celery on commit
        def trigger_request_notification():
            from .tasks import send_khidmat_request_notification_task
            safe_task_delay(send_khidmat_request_notification_task, khidmat_request_id, non_blocking=True)
            
        transaction.on_commit(trigger_request_notification)
        
        logger.info(f"Khidmat request created: {khidmat_request_id} - {serializer.data['request_type']}")
        
        return Response(
            {
                'success': True,
                'message': 'Request submitted successfully. Admin will review shortly.',
                'request_id': serializer.data['id']
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def approve(self, request, pk=None):
        """
        Approve a khidmat request.
        
        For cancellation requests:
        - Delete duty assignment
        - Update registration status to PENDING if no other duties
        - Cancel associated reminders
        
        For reallocation requests:
        - Mark as approved (admin will manually reassign)
        
        All updates are atomic to prevent partial state.
        """
        khidmat_request = self.get_object()
        
        if khidmat_request.status != 'pending':
            return Response(
                {'error': 'Request has already been processed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assignment = khidmat_request.assignment
        registration = assignment.assigned_user
        request_type = khidmat_request.request_type
        
        logger.info(f"Processing approval for request {pk}: {request_type} for user {registration.its_number}")
        
        # Capture data for notification BEFORE deletion
        snapshot_data = {
            'phone': registration.phone_number,
            'name': registration.full_name,
            'email': registration.email,
            'khidmat': assignment.get_namaaz_type_display(),
            'date': assignment.duty_date.strftime('%d %B %Y'),
            'reporting_time': get_reporting_time(assignment) or "N/A",
            'request_type': request_type
        }

        # Update request status FIRST (before deleting assignment)
        khidmat_request.status = 'approved'
        khidmat_request.reviewed_at = timezone.now()
        khidmat_request.reviewed_by_name = request.user.username if request.user.is_authenticated else 'Admin'
        khidmat_request.save()
        
        if request_type == 'cancel':
            # Store assignment details before deletion
            duty_date = assignment.duty_date
            namaaz_type = assignment.get_namaaz_type_display()
            
            # Cancel reminders for this assignment
            cancel_reminders_for_assignment(assignment)
            
            # Delete the duty assignment
            assignment.delete()
            logger.info(f"Deleted duty assignment: {duty_date} - {namaaz_type} for {registration.full_name}")
            
            # Check if user has any remaining duties
            remaining_duties = DutyAssignment.objects.filter(
                assigned_user=registration
            ).count()
            
            # Update registration status if no duties left
            if remaining_duties == 0:
                registration.status = 'PENDING'
                registration.save(update_fields=['status'])
                logger.info(f"Updated registration {registration.id} status to PENDING (no remaining duties)")
            else:
                logger.info(f"Registration {registration.id} still has {remaining_duties} remaining duties")
        
        # Trigger Notification (WhatsApp + Email) via Celery on commit
        def trigger_approval_notification():
            from .tasks import send_khidmat_approved_notification_task
            # Pass snapshot_data because assignment is deleted for 'cancel'
            safe_task_delay(send_khidmat_approved_notification_task, pk, snapshot_data, non_blocking=True)
            
        transaction.on_commit(trigger_approval_notification)

        logger.info(f"Khidmat request {pk} approved successfully")
        
        return Response({
            'success': True,
            'message': f'{request_type.capitalize()} request approved successfully.',
            'request_id': khidmat_request.id,
            'status': 'approved'
        })
    
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def reject(self, request, pk=None):
        """
        Reject a khidmat request.
        Only updates request status, no changes to duty roster.
        """
        khidmat_request = self.get_object()
        
        if khidmat_request.status != 'pending':
            return Response(
                {'error': 'Request has already been processed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update request status
        khidmat_request.status = 'rejected'
        khidmat_request.reviewed_at = timezone.now()
        khidmat_request.reviewed_by_name = request.user.username if request.user.is_authenticated else 'Admin'
        
        # Store admin note if provided
        admin_note = request.data.get('admin_note')
        if admin_note:
            khidmat_request.reason = f"{khidmat_request.reason}\n\nAdmin Note: {admin_note}"
        
        khidmat_request.save()
        
        logger.info(f"Khidmat request {pk} rejected by admin")
        
        return Response({
            'success': True,
            'message': 'Request rejected.',
            'request_id': khidmat_request.id,
            'status': 'rejected'
        })

class AuditionFileViewSet(viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin, viewsets.mixins.UpdateModelMixin):
    queryset = AuditionFile.objects.all()
    serializer_class = AuditionFileSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['patch'])
    def select_audition(self, request, pk=None):
        """
        Selects a specific audition file for a registration.
        Ensures only one file is selected per registration.
        """
        audition = self.get_object()
        registration = audition.registration
        
        try:
            with transaction.atomic():
                # Deselect all others for this registration
                registration.audition_files.update(is_selected=False)
                
                # Select the target
                audition.is_selected = True
                audition.save(update_fields=['is_selected'])
                
            return Response({'status': 'success', 'message': 'Audition selected'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CorrectionViewSet(viewsets.ModelViewSet):
    """
    API for managing Registration Corrections.
    """
    queryset = RegistrationCorrection.objects.all()
    serializer_class = RegistrationCorrectionSerializer
    
    def get_permissions(self):
        """
        Admin required for listing/creating.
        Public access allowed for retrieval/resolution via Token.
        """
        if self.action in ['retrieve_by_token', 'resolve_by_token']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]

    def create(self, request, *args, **kwargs):
        """
        Admin requests a correction.
        """
        registration_id = request.data.get('registration')
        field_name = request.data.get('field_name')
        
        # Verify Registration exists
        if not Registration.objects.filter(id=registration_id).exists():
            return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)
            
        # Create Correction
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        correction = serializer.save()
        
        # Trigger Notification (Email/WhatsApp) via Celery on commit
        def trigger_notification():
            from .tasks import send_correction_notification_task
            from .utils import safe_task_delay
            safe_task_delay(send_correction_notification_task, correction.id, non_blocking=True)
            
        transaction.on_commit(trigger_notification)
        
        logger.info(f"Correction requested for Reg {registration_id}, Field: {field_name}, Token: {correction.token}")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='token/(?P<token>[^/.]+)')
    def retrieve_by_token(self, request, token=None):
        """
        Public endpoint to get correction details by token.
        """
        try:
            correction = RegistrationCorrection.objects.get(token=token)
            
            if correction.status == 'RESOLVED':
                return Response({'error': 'This correction has already been resolved.'}, status=status.HTTP_400_BAD_REQUEST)
                
            return Response({
                'id': correction.id,
                'field_name': correction.field_name,
                'admin_message': correction.admin_message,
                'registration_name': correction.registration.full_name,
                'registration_its': correction.registration.its_number,
                'status': correction.status
            })
        except RegistrationCorrection.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='resolve/(?P<token>[^/.]+)')
    def resolve_by_token(self, request, token=None):
        """
        Public endpoint to resolve the correction.
        Updates the Registration model directly.
        """
        try:
            correction = RegistrationCorrection.objects.get(token=token)
            
            if correction.status == 'RESOLVED':
                return Response({'error': 'This correction has already been resolved.'}, status=status.HTTP_400_BAD_REQUEST)
            
            registration = correction.registration
            field_name = correction.field_name
            
            # Update the field on Registration
            # Handle special cases if necessary (e.g. file upload is handled by parser)
            
            if field_name == 'audition_files':
                files = request.FILES.getlist('audition_files')
                if not files:
                    return Response({'error': 'No files uploaded'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Logic to add files (create AuditionFile objects)
                for f in files:
                    AuditionFile.objects.create(registration=registration, audition_file_path=f)
                    
            else:
                # Standard field update
                new_value = request.data.get(field_name)
                if new_value is None:
                     return Response({'error': 'New value is required'}, status=status.HTTP_400_BAD_REQUEST)
                
                setattr(registration, field_name, new_value)
                registration.save(update_fields=[field_name])

            # Mark correction resolved
            correction.status = 'RESOLVED'
            correction.resolved_at = timezone.now()
            correction.save()
            
            # Trigger notification
            from .tasks import send_correction_completed_notification_task
            transaction.on_commit(lambda: send_correction_completed_notification_task.delay(registration.id))

            logger.info(f"Correction RESOLVED for Reg {registration.id}, Field: {field_name}")
            
            return Response({'status': 'success', 'message': 'Correction submitted successfully.'})
            
        except RegistrationCorrection.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

