from rest_framework import serializers
from .models import Registration, AuditionFile, DutyAssignment, UnlockLog, Reminder, ReminderLog


class AuditionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditionFile
        fields = ['id', 'audition_file_path', 'audition_file_type', 'audition_display_name', 'uploaded_at']
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
