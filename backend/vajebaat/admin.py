from django.contrib import admin
from .models import VajebaatMember, VajebaatForm, VajebaatAppointment


@admin.register(VajebaatMember)
class VajebaatMemberAdmin(admin.ModelAdmin):
    list_display = ('its_number', 'name', 'mohalla', 'mobile', 'created_at')
    search_fields = ('its_number', 'name', 'mohalla')
    list_filter = ('mohalla',)
    ordering = ('-created_at',)


@admin.register(VajebaatForm)
class VajebaatFormAdmin(admin.ModelAdmin):
    list_display = ('its_number', 'name', 'total', 'created_at')
    search_fields = ('its_number', 'name')
    ordering = ('-created_at',)
    readonly_fields = ('total',)


@admin.register(VajebaatAppointment)
class VajebaatAppointmentAdmin(admin.ModelAdmin):
    list_display = ('its_number', 'name', 'mobile', 'preferred_date', 'status', 'created_at')
    search_fields = ('its_number', 'name')
    list_filter = ('status', 'preferred_date')
    ordering = ('-created_at',)
