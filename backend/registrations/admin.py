"""
Django Admin configuration for Azaan & Takhbira Duty Management.
"""

from django.contrib import admin
from .models import (
    Registration, AuditionFile, DutyAssignment,
    UnlockLog, Reminder, ReminderLog
)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'its_number', 'email', 'phone_number', 'preference', 'is_active', 'created_at']
    list_filter = ['is_active', 'preference', 'created_at']
    search_fields = ['full_name', 'its_number', 'email']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    list_per_page = 100
    actions = ['hard_delete']

    def get_queryset(self, request):
        """Show all by default, but allow filtering by active status."""
        return super().get_queryset(request)

    def delete_model(self, request, obj):
        """Soft delete: mark as inactive instead of removing from DB."""
        obj.is_active = False
        obj.save()

    def delete_queryset(self, request, queryset):
        """Batch soft delete."""
        queryset.update(is_active=False)

    @admin.action(description="Hard Delete (Permanently remove from database)")
    def hard_delete(self, request, queryset):
        """Perform actual database deletion."""
        queryset.delete()


@admin.register(AuditionFile)
class AuditionFileAdmin(admin.ModelAdmin):
    list_display = ['audition_display_name', 'registration', 'audition_file_path', 'audition_file_type', 'uploaded_at']
    list_filter = ['audition_file_type', 'uploaded_at']
    search_fields = ['audition_display_name', 'registration__full_name', 'registration__its_number']
    readonly_fields = ['uploaded_at', 'audition_file_type', 'audition_display_name']


@admin.register(DutyAssignment)
class DutyAssignmentAdmin(admin.ModelAdmin):
    list_display = ['duty_date', 'namaaz_type', 'assigned_user', 'locked', 'locked_at']
    list_filter = ['namaaz_type', 'locked', 'duty_date']
    search_fields = ['assigned_user__full_name', 'assigned_user__its_number']
    readonly_fields = ['locked_at', 'created_at', 'updated_at']
    ordering = ['duty_date', 'namaaz_type']
    list_per_page = 100
    list_select_related = ['assigned_user']
    
    def get_readonly_fields(self, request, obj=None):
        """Make locked assignments read-only unless explicitly unlocked"""
        if obj and obj.locked:
            return self.readonly_fields + ('duty_date', 'namaaz_type', 'assigned_user', 'locked')
        return self.readonly_fields


@admin.register(UnlockLog)
class UnlockLogAdmin(admin.ModelAdmin):
    list_display = ['duty_date', 'namaaz_type', 'original_user_name', 'unlocked_by', 'unlocked_at']
    list_filter = ['unlocked_at', 'unlocked_by']
    search_fields = ['original_user_name', 'original_user_its', 'reason']
    readonly_fields = ['duty_assignment', 'unlocked_at', 'duty_date', 'namaaz_type', 
                       'original_user_name', 'original_user_its']
    ordering = ['-unlocked_at']
    
    def has_add_permission(self, request):
        """Prevent manual creation - logs are created automatically"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent editing - logs are immutable"""
        return False


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['duty_assignment', 'scheduled_datetime', 'status', 
                    'email_sent', 'whatsapp_sent', 'sent_at']
    list_filter = ['status', 'email_sent', 'whatsapp_sent', 'scheduled_datetime']
    search_fields = ['duty_assignment__assigned_user__full_name']
    readonly_fields = ['duty_assignment', 'scheduled_datetime', 'email_sent', 
                       'whatsapp_sent', 'sent_at', 'created_at']
    ordering = ['scheduled_datetime']
    list_per_page = 100
    list_select_related = ['duty_assignment', 'duty_assignment__assigned_user']
    
    def has_add_permission(self, request):
        """Prevent manual creation - reminders are created automatically"""
        return False


@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
    list_display = ['reminder', 'timestamp', 'channel', 'success', 'message']
    list_filter = ['channel', 'success', 'timestamp']
    search_fields = ['message']
    readonly_fields = ['reminder', 'timestamp', 'channel', 'success', 'message']
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        """Prevent manual creation - logs are created automatically"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent editing - logs are immutable"""
        return False
