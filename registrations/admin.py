"""
Django Admin configuration for Azaan & Takhbira Duty Management.
"""

from django.contrib import admin
from django.db import models
from .models import (
    Registration, AuditionFile, DutyAssignment,
    UnlockLog, Reminder, ReminderLog, AssignmentRequestLog
)

class PreferenceFilter(admin.SimpleListFilter):
    title = 'preference'
    parameter_name = 'preference'

    OPTIONS = [
        ('Azaan', 'Azaan'),
        ('Takhbira', 'Takhbira'),
        ('Sanah', 'Sanah'),
        ('Tajweed Quran Tilawat', 'Tajweed Quran Tilawat'),
        ('Dua e Joshan', 'Dua e Joshan'),
        ('Yaseen', 'Yaseen'),
    ]

    def lookups(self, request, model_admin):
        return self.OPTIONS

    def queryset(self, request, queryset):
        val = self.value()
        if not val:
            return queryset
        # Try JSON contains (new data) or icontains (legacy string)
        try:
            return queryset.filter(models.Q(preference__contains=[val]) | models.Q(preference__icontains=val))
        except Exception:
            # Fallback: try icontains only
            return queryset.filter(preference__icontains=val)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'its_number', 'email', 'phone_number', 'formatted_preference', 'created_at']
    # Use custom filter to support JSONField and legacy string values
    list_filter = [PreferenceFilter, 'created_at']
    search_fields = ['full_name', 'its_number', 'email']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    list_per_page = 100

    def formatted_preference(self, obj):
        try:
            prefs = obj.get_preference_list()
            return ", ".join(prefs) if prefs else ''
        except Exception:
            # Fallback to raw value
            return str(getattr(obj, 'preference', ''))
    formatted_preference.short_description = 'Preference'


@admin.register(AuditionFile)
class AuditionFileAdmin(admin.ModelAdmin):
    list_display = ['audition_display_name', 'registration', 'audition_file_path', 'audition_file_type', 'uploaded_at']
    list_filter = ['audition_file_type', 'uploaded_at']
    search_fields = ['audition_display_name', 'registration__full_name', 'registration__its_number']
    readonly_fields = ['uploaded_at', 'audition_file_type', 'audition_display_name']


@admin.register(DutyAssignment)
class DutyAssignmentAdmin(admin.ModelAdmin):
    list_display = ['duty_date', 'namaaz_type', 'assigned_user', 'status', 'locked', 'locked_at']
    list_filter = ['namaaz_type', 'status', 'locked', 'duty_date']
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


@admin.register(AssignmentRequestLog)
class AssignmentRequestLogAdmin(admin.ModelAdmin):
    list_display = ['duty_assignment', 'request_type', 'requested_by_its', 'requested_at', 'processed']
    list_filter = ['request_type', 'processed', 'requested_at']
    search_fields = ['duty_assignment__assigned_user__full_name', 'requested_by_its']
    readonly_fields = ['duty_assignment', 'request_type', 'requested_by_its', 'reason', 'preferred_datetime', 'requested_at']
    ordering = ['-requested_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
