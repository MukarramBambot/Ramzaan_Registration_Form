"""
API Views for Azaan & Takhbira Duty Management System.
Handles registration, duty assignment, unlocking, and reminders.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.utils import timezone
import logging

from .models import (
    Registration, AuditionFile, DutyAssignment, 
    UnlockLog, Reminder, ReminderLog, KhidmatRequest
)
from django.db.models import Q
from .serializers import (
    RegistrationSerializer, RegistrationCreateSerializer,
    AuditionFileSerializer, DutyAssignmentSerializer,
    DutyAssignmentCreateSerializer, UnlockSerializer,
    UnlockLogSerializer, ReminderSerializer, ReminderLogSerializer,
    KhidmatRequestSerializer
)
from .utils import (
    create_reminder_for_assignment, cancel_reminders_for_assignment,
    safe_task_delay
)
from .tasks import sync_to_sheets_task
from .tasks import send_registration_confirmation_task
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from django.utils import timezone
from django.db import transaction
from .tasks import notify_admin_cancel_request_task, notify_admin_reallocation_request_task
from .models import AssignmentRequestLog
from .utils.phone import normalize_phone_number


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
        Create new registration with audition file uploads.
        Max 5 audio files allowed.
        """
        import time
        start_time = time.time()
        logger.info("API: Registration create request received")

        try:
            # Check for duplicate ITS Number (manual check for custom error message)
            its_number = request.data.get('its_number')
            if Registration.objects.filter(its_number=its_number).exists():
                return Response(
                    {'error': f'ITS Number {its_number} is already registered.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check for duplicate Email
            email = request.data.get('email')
            if Registration.objects.filter(email=email).exists():
                return Response(
                    {'error': f'Email {email} is already registered.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate registration data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Create registration
            registration = serializer.save()
            
            # Handle uploaded media files. Accept both new key 'media_files' and legacy 'audition_files'
            files = request.FILES.getlist('media_files') or request.FILES.getlist('audition_files')

            # Validation: at least 1, maximum 6 audio files
            if len(files) > 6:
                return Response(
                    {'error': 'Maximum 6 audio files allowed'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if len(files) == 0:
                return Response(
                    {'error': 'At least 1 audio file required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Strict server-side MIME and size validation
            ALLOWED_AUDIO_TYPES = [
                'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/x-wav', 'audio/x-m4a', 'audio/m4a'
            ]
            MAX_BYTES = 10 * 1024 * 1024  # 10MB
            for f in files:
                ctype = getattr(f, 'content_type', '').lower()
                if ctype not in ALLOWED_AUDIO_TYPES:
                    return Response({'error': 'Only audio files are allowed'}, status=status.HTTP_400_BAD_REQUEST)
                if getattr(f, 'size', 0) > MAX_BYTES:
                    return Response({'error': 'Each file must be under 10MB'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Offload audition file creation and saving to background thread.
            # This ensures the API responds immediately (Step 1 required architecture).
            # Synchronous File Save (Production Fix)
            # Files must be saved before the request closes to prevent [Errno 2] on temp files.
            from .models import AuditionFile
            for file_obj in files:
                AuditionFile.objects.create(
                    registration=registration,
                    audition_file_path=file_obj
                )
            
            logger.info(f"Saved {len(files)} user uploaded files synchronously.")
            
            # Background notifications & Sheet sync are now handled automatically 
            # via Django signals for better decoupled logic.
            
            # Return full registration data
            output_serializer = RegistrationSerializer(registration)
            
            logger.info(f"New registration created: {registration}")
            
            return Response(
                output_serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            return Response(
                {'error': 'Registration failed. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            duration = time.time() - start_time
            logger.info(f"API: Registration create finished in {duration:.4f}s")
    
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
            # Optimize with prefetch
            registration = Registration.objects.prefetch_related(
                'duty_assignments', 
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

                pending_req = duty.requests.filter(status='pending').first()
                duties.append({
                    "id": duty.id,
                    "date": duty.duty_date.strftime('%d/%m/%Y'),
                    "namaaz": namaaz,
                    "type": duty_type,
                    "status": duty.status,
                    "request_status": pending_req.status if pending_req else None,
                    "request_type": pending_req.request_type if pending_req else None
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

    @action(detail=True, methods=['get'])
    def audition_files(self, request, pk=None):
        """Get audition files for a specific registration"""
        registration = self.get_object()
        files = registration.audition_files.all()
        serializer = AuditionFileSerializer(files, many=True)
        return Response(serializer.data)

# ==========================================
# ADMIN ENDPOINTS: KHIDMAT REQUESTS
# ==========================================

class KhidmatRequestAdminListView(APIView):
    """Admin-only endpoint to list pending KhidmatRequests."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        status_filter = request.query_params.get('status', 'pending')
        requests = KhidmatRequest.objects.filter(status=status_filter).select_related(
            'assignment', 
            'assignment__assigned_user'
        )
        serializer = KhidmatRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class KhidmatRequestApproveView(APIView):
    """Admin-only endpoint to approve a KhidmatRequest."""
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request, pk):
        try:
             khidmat_req = KhidmatRequest.objects.select_for_update().get(id=pk)
        except KhidmatRequest.DoesNotExist:
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

        if khidmat_req.status != 'pending':
            return Response({'error': f'Request already {khidmat_req.status}'}, status=status.HTTP_400_BAD_REQUEST)

        assignment = khidmat_req.assignment

        if khidmat_req.request_type == 'cancel':
            # Approve Cancellation
            assignment.status = 'cancelled'
            assignment.locked = False
            # Clear reminder if exists
            cancel_reminders_for_assignment(assignment)
            assignment.save(update_fields=['status', 'locked'])
            logger.info(f"ADMIN: Cancellation Approved for {assignment}")

        elif khidmat_req.request_type == 'reallocate':
            # Approve Reallocation
            if khidmat_req.preferred_date:
                assignment.duty_date = khidmat_req.preferred_date
            if khidmat_req.preferred_time:
                assignment.namaaz_type = khidmat_req.preferred_time
            
            # Keep status as confirmed, or maybe set to pending if we want them to re-confirm?
            # Requirement says: "Keep status = confirmed"
            assignment.status = 'confirmed'
            
            # Re-generate reminder for the new date
            cancel_reminders_for_assignment(assignment)
            create_reminder_for_assignment(assignment)
            
            assignment.save(update_fields=['duty_date', 'namaaz_type', 'status'])
            logger.info(f"ADMIN: Reallocation Approved for {assignment}")

        # Finalize Request status
        khidmat_req.status = 'approved'
        khidmat_req.reviewed_at = timezone.now()
        khidmat_req.reviewed_by_name = request.user.get_full_name() or request.user.username
        khidmat_req.save()

        # Mark audit log as processed
        AssignmentRequestLog.objects.filter(duty_assignment=assignment, processed=False).update(processed=True)

        return Response({'message': f'{khidmat_req.get_request_type_display()} request approved'}, status=status.HTTP_200_OK)


class KhidmatRequestRejectView(APIView):
    """Admin-only endpoint to reject a KhidmatRequest."""
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request, pk):
        try:
             khidmat_req = KhidmatRequest.objects.select_for_update().get(id=pk)
        except KhidmatRequest.DoesNotExist:
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

        if khidmat_req.status != 'pending':
            return Response({'error': f'Request already {khidmat_req.status}'}, status=status.HTTP_400_BAD_REQUEST)

        khidmat_req.status = 'rejected'
        khidmat_req.reviewed_at = timezone.now()
        khidmat_req.reviewed_by_name = request.user.get_full_name() or request.user.username
        khidmat_req.save()

        # Mark audit log as processed (rejected requests are also processed)
        AssignmentRequestLog.objects.filter(duty_assignment=khidmat_req.assignment, processed=False).update(processed=True)

        logger.info(f"ADMIN: {khidmat_req.get_request_type_display()} REJECTED for {khidmat_req.assignment}")
        return Response({'message': 'Request rejected'}, status=status.HTTP_200_OK)


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
            locked=True,
            status='confirmed'
        )
        
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
    
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def cancel(self, request, pk=None):
        """Register a cancellation request for this assignment."""
        assignment = self.get_object()
        
        if assignment.status != 'confirmed':
            return Response({'error': 'Action allowed only on confirmed assignments'}, status=status.HTTP_400_BAD_REQUEST)
        
        if KhidmatRequest.objects.filter(assignment=assignment, status='pending').exists():
            return Response({'error': 'A request is already pending for this assignment'}, status=status.HTTP_400_BAD_REQUEST)

        KhidmatRequest.objects.create(
            assignment=assignment,
            request_type='cancel'
        )
        
        # Notify admin asynchronously
        try:
            safe_task_delay(notify_admin_cancel_request_task, assignment.id, non_blocking=True)
        except Exception as e:
            logger.error(f"Failed to enqueue admin cancel notification: {str(e)}")

        return Response({'message': 'Cancellation request submitted'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def reallocate(self, request, pk=None):
        """Register a reallocation request for this assignment."""
        assignment = self.get_object()
        
        if assignment.status != 'confirmed':
            return Response({'error': 'Action allowed only on confirmed assignments'}, status=status.HTTP_400_BAD_REQUEST)
        
        if KhidmatRequest.objects.filter(assignment=assignment, status='pending').exists():
            return Response({'error': 'A request is already pending for this assignment'}, status=status.HTTP_400_BAD_REQUEST)

        KhidmatRequest.objects.create(
            assignment=assignment,
            request_type='reallocate'
        )
        
        try:
            safe_task_delay(notify_admin_reallocation_request_task, assignment.id, non_blocking=True)
        except Exception as e:
            logger.error(f"Failed to enqueue admin reallocation notification: {str(e)}")

        return Response({'message': 'Reallocation request submitted'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def unlock(self, request, pk=None):
        """
        Emergency unlock a locked duty assignment.
        Requires mandatory reason.
        """
        assignment = self.get_object()
        
        if not assignment.locked:
            return Response(
                {'error': 'This duty is not locked'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate unlock reason
        unlock_serializer = UnlockSerializer(data=request.data)
        unlock_serializer.is_valid(raise_exception=True)
        
        reason = unlock_serializer.validated_data['reason']
        
        # Create unlock log
        unlock_log = UnlockLog.objects.create(
            duty_assignment=assignment,
            reason=reason,
            unlocked_by=request.user.username if request.user.is_authenticated else "Admin",
            duty_date=assignment.duty_date,
            namaaz_type=assignment.namaaz_type,
            original_user_name=assignment.assigned_user.full_name,
            original_user_its=assignment.assigned_user.its_number
        )
        
        # Cancel existing reminders
        cancel_reminders_for_assignment(assignment)
        
        # Delete the assignment
        assignment.delete()
        
        logger.info(f"Emergency unlock: {unlock_log}")
        
        return Response({
            'message': 'Duty unlocked successfully',
            'unlock_log_id': unlock_log.id
        })
    
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
            
            grid_data[date_key][assignment.namaaz_type] = {
                'id': assignment.id,
                'user_id': assignment.assigned_user.id,
                'user_name': assignment.assigned_user.full_name,
                'user_its': assignment.assigned_user.its_number,
                'user_email': assignment.assigned_user.email,
                'user_phone': assignment.assigned_user.phone_number,
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
