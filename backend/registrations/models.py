from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os
import re
import uuid

class Registration(models.Model):
    """
    User registration for Azaan & Takhbira duties.
    """
    DUTY_CHOICES = [
        ('AZAAN', 'Azaan'),
        ('TAKHBIRA', 'Takhbira'),
        ('SANAH', 'Sanah'),
        ('TILAWAT', 'Tajwid Quran Majid Tilawat'),
        ('JOSHAN', 'Dua e Joshan'),
        ('YASEEN', 'Yaseen'),
        ('BOTH', 'Both'),
    ]
    
    full_name = models.CharField(max_length=255)
    its_number = models.CharField(max_length=20, unique=True, help_text="Unique ITS Number")
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, help_text="WhatsApp Number with country code")
    preference = models.JSONField(default=list) # Reverted to JSONField as per DB
    status = models.CharField(
        max_length=20, 
        choices=[('PENDING', 'Pending'), ('ALLOTTED', 'Allotted')],
        default='PENDING'
    )
    
    # WhatsApp tracking fields
    whatsapp_sent = models.BooleanField(default=False)
    whatsapp_delivered_at = models.DateTimeField(null=True, blank=True)
    whatsapp_error = models.TextField(null=True, blank=True)
    whatsapp_message_id = models.CharField(max_length=100, null=True, blank=True)
    whatsapp_read_at = models.DateTimeField(null=True, blank=True)
    whatsapp_status = models.CharField(max_length=20, default='none')
    whatsapp_failed_reason = models.TextField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True, help_text="Soft delete flag")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['its_number']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.full_name} ({self.its_number})"

    def get_preference_display(self):
        """
        Custom display for JSONField preferences.
        Maps canonical keys to human-readable labels.
        """
        if not isinstance(self.preference, list):
            return str(self.preference)
            
        choices_dict = dict(self.DUTY_CHOICES)
        display_list = [choices_dict.get(p, p) for p in self.preference]
        return ", ".join(display_list)


def audition_file_path(instance, filename):
    """
    Standardizes file naming and path.
    """
    its = instance.registration.its_number
    name = instance.registration.full_name.lower().replace(' ', '_')
    name = re.sub(r'[^a-z0-9_]', '', name)
    
    # Handle preference if it's a list (JSON)
    pref_str = "both"
    if isinstance(instance.registration.preference, list) and instance.registration.preference:
        pref_str = "_".join(instance.registration.preference).lower()
    
    ext = filename.split('.')[-1].lower()
    new_filename = f"{its}_{name}_{pref_str}.{ext}"
    subfolder = 'audio' if ext in ['mp3', 'wav', 'm4a', 'aac'] else 'video'
    
    return os.path.join('auditions files', subfolder, new_filename)

class AuditionFile(models.Model):
    FILE_TYPES = [('audio', 'Audio'), ('video', 'Video')]

    registration = models.ForeignKey(
        Registration, 
        related_name='audition_files', 
        on_delete=models.CASCADE
    )
    audition_file_path = models.FileField(
        upload_to=audition_file_path,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'm4a', 'aac', 'mp4', 'mov', 'webm', 'ogg'])],
        default=""
    )
    audition_file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='audio')
    audition_display_name = models.CharField(max_length=255, default='')
    is_selected = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.audition_display_name

    def save(self, *args, **kwargs):
        if not self.audition_file_type:
            ext = self.audition_file_path.name.split('.')[-1].lower()
            self.audition_file_type = 'audio' if ext in ['mp3', 'wav', 'm4a', 'aac'] else 'video'
        
        if not self.audition_display_name:
            self.audition_display_name = f"{self.registration.full_name} – Audition"
            
        super().save(*args, **kwargs)


class DutyAssignment(models.Model):
    NAMAAZ_CHOICES = [
        ('SANAH', 'Sanah'),
        ('TAJWEED', 'Tajwid Quran Majid Tilawat'),
        ('DUA_E_JOSHAN', 'Dua e Joshan'),
        ('YASEEN', 'Yaseen'),
        ('FAJAR_AZAAN', 'Fajar Azaan'),
        ('FAJAR_TAKBIRA', 'Fajar Takbira'),
        ('ZOHAR_AZAAN', 'Zohar Azaan'),
        ('ZOHAR_TAKBIRA', 'Zohar Takbira'),
        ('ASAR_TAKBIRA', 'Asar Takbira'),
        ('MAGRIB_AZAAN', 'Magrib Azaan'),
        ('MAGRIB_TAKBIRA', 'Magrib Takbira'),
        ('ISHAA_TAKBIRA', 'Ishaa Takbira'),
    ]
    
    duty_date = models.DateField()
    namaaz_type = models.CharField(max_length=20, choices=NAMAAZ_CHOICES)
    assigned_user = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        related_name='duty_assignments'
    )
    locked = models.BooleanField(default=True)
    allotment_notification_sent = models.BooleanField(default=False)
    locked_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields from DB
    status = models.CharField(max_length=50, default='allotted')
    cancel_reason = models.TextField(blank=True, null=True)
    reallocation_reason = models.TextField(blank=True, null=True)
    reallocation_requested_at = models.DateTimeField(blank=True, null=True)
    cancel_requested_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('duty_date', 'namaaz_type')
        ordering = ['duty_date', 'namaaz_type']
        indexes = [
            models.Index(fields=['duty_date']),
            models.Index(fields=['namaaz_type']),
        ]
    
    def __str__(self):
        return f"{self.duty_date} - {self.namaaz_type} → {self.assigned_user.full_name}"


class UnlockLog(models.Model):
    duty_assignment = models.ForeignKey(
        DutyAssignment,
        on_delete=models.SET_NULL,
        null=True,
        related_name='unlock_logs'
    )
    unlocked_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    unlocked_by = models.CharField(max_length=255, default="Admin")
    duty_date = models.DateField()
    namaaz_type = models.CharField(max_length=20)
    original_user_name = models.CharField(max_length=255)
    original_user_its = models.CharField(max_length=20)
    
    class Meta:
        ordering = ['-unlocked_at']


class Reminder(models.Model):
    duty_assignment = models.OneToOneField(
        DutyAssignment,
        on_delete=models.CASCADE,
        related_name='reminder'
    )
    scheduled_datetime = models.DateTimeField()
    email_sent = models.BooleanField(default=False)
    whatsapp_sent = models.BooleanField(default=False)
    whatsapp_status = models.CharField(max_length=20, default='none')
    whatsapp_message_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, default='PENDING')
    email_attempts = models.IntegerField(default=0)
    whatsapp_attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True)
    
    class Meta:
        ordering = ['scheduled_datetime']


class ReminderLog(models.Model):
    reminder = models.ForeignKey(
        Reminder,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    channel = models.CharField(max_length=20)
    success = models.BooleanField()
    message = models.TextField()
    
    class Meta:
        ordering = ['-timestamp']


class KhidmatRequest(models.Model):
    assignment = models.ForeignKey(
        DutyAssignment, 
        on_delete=models.CASCADE, 
        related_name='requests'
    )
    request_type = models.CharField(max_length=20)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.CharField(max_length=20, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


class AssignmentRequestLog(models.Model):
    request_type = models.CharField(max_length=20)
    requested_by_its = models.CharField(max_length=20)
    reason = models.TextField(null=True, blank=True)
    preferred_datetime = models.CharField(max_length=255, null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    duty_assignment = models.ForeignKey(
        DutyAssignment, 
        on_delete=models.CASCADE,
        related_name='request_logs'
    )

class RegistrationCorrection(models.Model):
    """
    Tracks correction requests from Admins to Users.
    No data is deleted; users are given a token to update specific fields.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RESOLVED', 'Resolved'),
    ]

    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='corrections')
    field_name = models.CharField(max_length=100, help_text="Field needing correction (e.g., 'full_name', 'audition_files')")
    admin_message = models.TextField(help_text="Message from admin explaining what to fix")
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

class DutyReminderCall(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    duty_assignment = models.ForeignKey(DutyAssignment, on_delete=models.CASCADE, related_name='voice_reminders', null=True)
    scheduled_time = models.DateTimeField()
    call_status = models.CharField(max_length=50, default="PENDING")
    exotel_call_sid = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('registration', 'scheduled_time')

    def __str__(self):
        return f"Call for {self.registration.its_number} at {self.scheduled_time}"

