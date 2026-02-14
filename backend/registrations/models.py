from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import pytz
import os
import re

class Registration(models.Model):
    """
    User registration for Azaan & Takhbira duties.
    This data is READ-ONLY after submission.
    """
    DUTY_CHOICES = [
        ('AZAAN', 'Azaan'),
        ('TAKHBIRA', 'Takhbira'),
        ('BOTH', 'Both'),
    ]
    
    full_name = models.CharField(max_length=255)
    its_number = models.CharField(max_length=20, unique=True, help_text="Unique ITS Number")
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, help_text="WhatsApp Number with country code (e.g., +919876543210)")
    preference = models.CharField(max_length=10, choices=DUTY_CHOICES)
    status = models.CharField(
        max_length=20, 
        choices=[('PENDING', 'Pending'), ('ALLOTTED', 'Allotted')],
        default='PENDING',
        db_default='PENDING'
    )
    whatsapp_sent = models.BooleanField(default=False, help_text="Track initial registration WhatsApp")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['its_number']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.full_name} ({self.its_number})"


def audition_file_path(instance, filename):
    """
    Standardizes file naming and path:
    auditions files/<audio|video>/<ITS>_<full_name>_<register_for>.<extension>
    """
    its = instance.registration.its_number
    # Clean name: lowercase and underscores
    name = instance.registration.full_name.lower().replace(' ', '_')
    name = re.sub(r'[^a-z0-9_]', '', name)
    
    pref = instance.registration.preference.lower()
    ext = filename.split('.')[-1].lower()
    
    # Standardize filename
    new_filename = f"{its}_{name}_{pref}.{ext}"
    
    # Determine subfolder
    subfolder = 'audio' if ext in ['mp3', 'wav', 'm4a', 'aac'] else 'video'
    
    return os.path.join('auditions files', subfolder, new_filename)

class AuditionFile(models.Model):
    """
    Audition files (audio/video) for registrations.
    Stored on disk in categorized folders.
    """
    FILE_TYPES = [('audio', 'Audio'), ('video', 'Video')]

    registration = models.ForeignKey(
        Registration, 
        related_name='audition_files', 
        on_delete=models.CASCADE
    )
    # audition_file_path in MySQL
    audition_file_path = models.FileField(
        upload_to=audition_file_path,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'm4a', 'aac', 'mp4', 'mov', 'webm', 'ogg'])],
        default=""
    )
    # audition_file_type
    audition_file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='audio')
    # audition_display_name
    audition_display_name = models.CharField(max_length=255, default='')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.audition_display_name

    def save(self, *args, **kwargs):
        # Set audition_file_type and audition_display_name before saving
        if not self.audition_file_type:
            ext = self.audition_file_path.name.split('.')[-1].lower()
            self.audition_file_type = 'audio' if ext in ['mp3', 'wav', 'm4a', 'aac'] else 'video'
        
        if not self.audition_display_name:
            pref_label = self.registration.get_preference_display()
            self.audition_display_name = f"{self.registration.full_name} – {pref_label} Audition"
            
        super().save(*args, **kwargs)


class DutyAssignment(models.Model):
    """
    Excel-style duty roster.
    Each assignment = ONE date + ONE namaaz + ONE user.
    Once assigned, it is LOCKED by default.
    """
    NAMAAZ_CHOICES = [
        ('FAJAR_AZAAN', 'Fajar Azaan'),
        ('FAJAR_TAKBIRA', 'Fajar Takbira'),
        ('ZOHAR_AZAAN', 'Zohar Azaan'),
        ('ZOHAR_TAKBIRA', 'Zohar Takbira'),
        ('ASAR_TAKBIRA', 'Asar Takbira'),
        ('MAGRIB_AZAAN', 'Magrib Azaan'),
        ('MAGRIB_TAKBIRA', 'Magrib Takbira'),
        ('ISHAA_TAKBIRA', 'Ishaa Takbira'),
    ]
    
    duty_date = models.DateField(help_text="Date of the duty")
    namaaz_type = models.CharField(max_length=20, choices=NAMAAZ_CHOICES)
    assigned_user = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        related_name='duty_assignments'
    )
    locked = models.BooleanField(default=True, help_text="Locked duties cannot be changed without unlock")
    allotment_notification_sent = models.BooleanField(default=False, help_text="Track allotment WhatsApp notification")
    locked_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Ensure ONE user per duty slot (no duplicate assignments)
        unique_together = ('duty_date', 'namaaz_type')
        ordering = ['duty_date', 'namaaz_type']
        indexes = [
            models.Index(fields=['duty_date']),
            models.Index(fields=['namaaz_type']),
        ]
    
    def __str__(self):
        return f"{self.duty_date} - {self.get_namaaz_type_display()} → {self.assigned_user.full_name}"


class UnlockLog(models.Model):
    """
    Audit trail for emergency unlocks.
    Tracks who unlocked, when, and why.
    """
    duty_assignment = models.ForeignKey(
        DutyAssignment,
        on_delete=models.SET_NULL,
        null=True,
        related_name='unlock_logs'
    )
    unlocked_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(help_text="Mandatory reason for emergency unlock")
    unlocked_by = models.CharField(max_length=255, default="Admin", help_text="Who performed the unlock")
    
    # Store duty details in case assignment is deleted
    duty_date = models.DateField()
    namaaz_type = models.CharField(max_length=20)
    original_user_name = models.CharField(max_length=255)
    original_user_its = models.CharField(max_length=20)
    
    class Meta:
        ordering = ['-unlocked_at']
    
    def __str__(self):
        return f"Unlock: {self.duty_date} - {self.namaaz_type} at {self.unlocked_at}"


class Reminder(models.Model):
    """
    Automatic reminder scheduling.
    ONE REMINDER per duty assignment.
    Sent 1 day before at configured time (6 PM or 12 AM).
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    duty_assignment = models.OneToOneField(
        DutyAssignment,
        on_delete=models.CASCADE,
        related_name='reminder'
    )
    
    # When to send the reminder (1 day before at fixed time)
    scheduled_datetime = models.DateTimeField(help_text="When to send this reminder")
    
    # Tracking flags
    email_sent = models.BooleanField(default=False)
    whatsapp_sent = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    # Retry tracking
    email_attempts = models.IntegerField(default=0)
    whatsapp_attempts = models.IntegerField(default=0)
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Error logging
    last_error = models.TextField(blank=True)
    
    class Meta:
        ordering = ['scheduled_datetime']
        indexes = [
            models.Index(fields=['status', 'scheduled_datetime']),
        ]
    
    def __str__(self):
        return f"Reminder for {self.duty_assignment} - {self.status}"
    
    def mark_sent(self):
        """Mark reminder as successfully sent"""
        self.status = 'SENT'
        self.sent_at = timezone.now()
        self.save()
    
    def mark_failed(self, error_message):
        """Mark reminder as failed with error"""
        self.status = 'FAILED'
        self.last_error = error_message
        self.save()
    
    def cancel(self):
        """Cancel reminder (used when duty is reassigned)"""
        self.status = 'CANCELLED'
        self.save()


class ReminderLog(models.Model):
    """
    Detailed log of all reminder sends.
    For debugging and audit trail.
    """
    reminder = models.ForeignKey(
        Reminder,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    channel = models.CharField(max_length=20, choices=[('EMAIL', 'Email'), ('WHATSAPP', 'WhatsApp')])
    success = models.BooleanField()
    message = models.TextField()
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        status = "✓" if self.success else "✗"
        return f"{status} {self.channel} - {self.reminder.duty_assignment}"
