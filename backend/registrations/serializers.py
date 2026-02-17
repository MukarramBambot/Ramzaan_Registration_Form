from rest_framework import serializers
from .models import Registration, AuditionFile, DutyAssignment, UnlockLog, Reminder, ReminderLog, KhidmatRequest, RegistrationCorrection


class AuditionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditionFile
        fields = ['id', 'audition_file_path', 'audition_file_type', 'audition_display_name', 'is_selected', 'uploaded_at']
        read_only_fields = ['uploaded_at', 'audition_file_type', 'audition_display_name']


class RegistrationSerializer(serializers.ModelSerializer):
    audition_files = AuditionFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = Registration
        fields = [
            'id',
            'full_name',
            'its_number',
            'email',
            'phone_number',
            'preference',
            'status',
            'created_at',
            'audition_files'
        ]
        read_only_fields = ['created_at']


class RegistrationCreateSerializer(serializers.ModelSerializer):
    """Separate serializer for creating registrations with file uploads"""
    # Use ListField to handle multiple 'preference' values from FormData
    preference = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        min_length=1
    )

    class Meta:
        model = Registration
        fields = [
            'full_name',
            'its_number',
            'email',
            'phone_number',
            'preference',
            'status'
        ]
        extra_kwargs = {
            'status': {'default': 'PENDING'}
        }

    def to_internal_value(self, data):
        """
        Ensure 'preference' is always treated as a list even if multiple keys are sent.
        Avoids QueryDict.copy() which crashes on files (BufferedRandom pickling error).
        """
        if hasattr(data, 'getlist'):
            # Convert QueryDict to a plain dict to avoid recursive deepcopy of file handles
            new_data = data.dict()
            prefs = data.getlist('preference')
            if prefs:
                new_data['preference'] = prefs
            data = new_data
        
        return super().to_internal_value(data)

    def validate_preference(self, value):
        """
        Normalize and validate against Registration.DUTY_CHOICES.
        Maps frontend strings to backend keys.
        Supports:
        - "Azaan" -> "AZAAN"
        - ["Azaan", "Takhbira"] -> ["AZAAN", "TAKHBIRA"]
        - "Sanah" -> ["SANAH"]
        - "Tajweed Quran Tilawat" -> ["TILAWAT"]
        - "Dua e Joshan" -> ["JOSHAN"]
        - "Yaseen" -> ["YASEEN"]
        """
        if isinstance(value, str):
            value = [value]

        if not isinstance(value, list):
            raise serializers.ValidationError("Preference must be a list or string.")

        normalized = []
        # Mapping from frontend values (case-insensitive) to backend keys
        mapping = {
            'AZAAN': 'AZAAN',
            'TAKHBIRA': 'TAKHBIRA',
            'TAKBIRA': 'TAKHBIRA',
            'SANAH': 'SANAH',
            'TAJWEED QURAN TILAWAT': 'TILAWAT',
            'TAJWEED QURAN MASJID TILAWAT': 'TILAWAT',
            'TAJWID QURAN TILAWAT': 'TILAWAT',
            'TAJWID QURAN MAJID TILAWAT': 'TILAWAT',
            'DUA E JOSHAN': 'JOSHAN',
            'DUA E JOSHEN': 'JOSHAN',
            'YASEEN': 'YASEEN',
            'BOTH': 'BOTH'
        }
        
        valid_choices = dict(Registration.DUTY_CHOICES)
        valid_keys = list(valid_choices.keys())
        
        for item in value:
            if not isinstance(item, str):
                continue
            
            item_clean = item.strip().upper()
            mapped_key = mapping.get(item_clean, item_clean)
            
            if mapped_key not in valid_keys:
                raise serializers.ValidationError(f"'{item}' is not a valid choice.")
            normalized.append(mapped_key)
            
        if not normalized:
            raise serializers.ValidationError("At least one valid preference is required.")

        return list(set(normalized))


class DutyAssignmentSerializer(serializers.ModelSerializer):
    assigned_user_name = serializers.CharField(source='assigned_user.full_name', read_only=True)
    assigned_user_its = serializers.CharField(source='assigned_user.its_number', read_only=True)
    assigned_user_email = serializers.EmailField(source='assigned_user.email', read_only=True)
    assigned_user_phone = serializers.CharField(source='assigned_user.phone_number', read_only=True)
    namaaz_display = serializers.CharField(source='get_namaaz_type_display', read_only=True)
    
    class Meta:
        model = DutyAssignment
        fields = [
            'id',
            'duty_date',
            'namaaz_type',
            'namaaz_display',
            'assigned_user',
            'assigned_user_name',
            'assigned_user_its',
            'assigned_user_email',
            'assigned_user_phone',
            'locked',
            'locked_at',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['locked', 'locked_at', 'created_at', 'updated_at']


class DutyAssignmentCreateSerializer(serializers.Serializer):
    """Serializer for creating duty assignments"""
    duty_date = serializers.DateField()
    namaaz_type = serializers.ChoiceField(choices=DutyAssignment.NAMAAZ_CHOICES)
    assigned_user_id = serializers.IntegerField()
    
    def validate_assigned_user_id(self, value):
        """Ensure user exists"""
        if not Registration.objects.filter(id=value).exists():
            raise serializers.ValidationError("User not found")
        return value
    
    def validate(self, data):
        """Check for duplicate assignments"""
        exists = DutyAssignment.objects.filter(
            duty_date=data['duty_date'],
            namaaz_type=data['namaaz_type']
        ).exists()
        
        if exists:
            raise serializers.ValidationError(
                "This duty slot is already assigned. Unlock it first to reassign."
            )
        
        return data


class UnlockSerializer(serializers.Serializer):
    """Serializer for emergency unlock requests"""
    reason = serializers.CharField(
        required=True,
        allow_blank=False,
        help_text="Mandatory reason for emergency unlock"
    )
    
    def validate_reason(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Reason must be at least 10 characters"
            )
        return value.strip()


class UnlockLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnlockLog
        fields = [
            'id',
            'duty_assignment',
            'unlocked_at',
            'reason',
            'unlocked_by',
            'duty_date',
            'namaaz_type',
            'original_user_name',
            'original_user_its'
        ]


class ReminderSerializer(serializers.ModelSerializer):
    duty_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Reminder
        fields = [
            'id',
            'duty_details',
            'scheduled_datetime',
            'email_sent',
            'whatsapp_sent',
            'status',
            'email_attempts',
            'whatsapp_attempts',
            'created_at',
            'sent_at',
            'last_error'
        ]
    
    def get_duty_details(self, obj):
        return {
            'date': obj.duty_assignment.duty_date,
            'namaaz': obj.duty_assignment.get_namaaz_type_display(),
            'user_name': obj.duty_assignment.assigned_user.full_name,
            'user_its': obj.duty_assignment.assigned_user.its_number
        }


class ReminderLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReminderLog
        fields = [
            'id',
            'reminder',
            'timestamp',
            'channel',
            'success',
            'message'
        ]


class KhidmatRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for Khidmat (duty) cancellation and reallocation requests.
    Supports both user-initiated requests and admin review actions.
    """
    user_details = serializers.SerializerMethodField()
    assignment_details = serializers.SerializerMethodField()
    request_type_display = serializers.SerializerMethodField()
    
    # For creating requests, accept assignment_id instead of assignment object
    assignment_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = KhidmatRequest
        fields = [
            'id', 'assignment', 'assignment_id', 'request_type', 'reason', 
            'status', 'created_at', 'reviewed_at', 'reviewed_by_name',
            'user_details', 'assignment_details', 'request_type_display',
            'preferred_date', 'preferred_time'
        ]
        read_only_fields = ['created_at', 'reviewed_at', 'assignment']
        extra_kwargs = {
            'assignment': {'required': False}
        }
    
    def get_user_details(self, obj):
        """Return user information from the assignment"""
        if not obj.assignment:
            return None
        user = obj.assignment.assigned_user
        return {
            'full_name': user.full_name,
            'its_number': user.its_number,
            'phone_number': user.phone_number
        }
    
    def get_assignment_details(self, obj):
        """Return duty assignment details"""
        if not obj.assignment:
            return None
        return {
            'date': obj.assignment.duty_date.strftime('%d/%m/%Y'),
            'namaaz': obj.assignment.get_namaaz_type_display()
        }
    
    def get_request_type_display(self, obj):
        """Return human-readable request type"""
        return 'Cancellation' if obj.request_type == 'cancel' else 'Reallocation'
    
    def validate(self, data):
        """
        Validate the request:
        - assignment_id must exist
        - User must have an active duty assignment
        - Only one pending request allowed per assignment
        - Request type must be valid
        """
        # Get assignment_id from data
        assignment_id = data.get('assignment_id')
        
        if assignment_id:
            # Verify assignment exists
            try:
                assignment = DutyAssignment.objects.get(id=assignment_id)
            except DutyAssignment.DoesNotExist:
                raise serializers.ValidationError({
                    'assignment_id': 'Duty assignment not found.'
                })
            
            # Check for existing pending request for this assignment
            existing_request = KhidmatRequest.objects.filter(
                assignment=assignment,
                status='pending'
            ).first()
            
            if existing_request:
                raise serializers.ValidationError({
                    'assignment_id': 'A pending request already exists for this duty assignment.'
                })
            
            # Store assignment in validated data
            data['assignment'] = assignment
        
        # Validate request_type
        request_type = data.get('request_type')
        if request_type not in ['cancel', 'reallocate']:
            raise serializers.ValidationError({
                'request_type': 'Request type must be either "cancel" or "reallocate".'
            })
        
        return data
    
    def create(self, validated_data):
        """Create a new khidmat request"""
        # Remove assignment_id from validated_data (we already set assignment)
        validated_data.pop('assignment_id', None)
        return super().create(validated_data)


class RegistrationCorrectionSerializer(serializers.ModelSerializer):
    """
    Serializer for Correction Requests.
    """
    registration_its = serializers.CharField(source='registration.its_number', read_only=True)
    registration_name = serializers.CharField(source='registration.full_name', read_only=True)

    class Meta:
        model = RegistrationCorrection
        fields = [
            'id', 'registration', 'registration_its', 'registration_name',
            'field_name', 'admin_message', 'token', 'status',
            'created_at', 'resolved_at'
        ]
        read_only_fields = ['token', 'created_at', 'resolved_at']

