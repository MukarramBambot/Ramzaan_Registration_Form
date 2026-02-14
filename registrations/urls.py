"""
URL routing for Azaan & Takhbira API endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .webhook_views import whatsapp_webhook
from .views import (
    RegistrationViewSet,
    DutyAssignmentViewSet,
    UnlockLogViewSet,
    ReminderViewSet,
    ReminderLogViewSet,
    MeView,
    HealthCheckView,
    KhidmatRequestAdminListView,
    KhidmatRequestApproveView,
    KhidmatRequestRejectView
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'registrations', RegistrationViewSet, basename='registration')
router.register(r'duty-assignments', DutyAssignmentViewSet, basename='duty-assignment')
router.register(r'unlock-logs', UnlockLogViewSet, basename='unlock-log')
router.register(r'reminders', ReminderViewSet, basename='reminder')
router.register(r'reminder-logs', ReminderLogViewSet, basename='reminder-log')

urlpatterns = [
    path('auth/me/', MeView.as_view(), name='me'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('webhooks/whatsapp/', whatsapp_webhook, name='whatsapp_webhook'),
    
    # Direct Assignment Requests (Simplified Workflow)
    path('assignments/<int:pk>/cancel/', DutyAssignmentViewSet.as_view({'post': 'cancel'}), name='assignment-cancel'),
    path('assignments/<int:pk>/reallocate/', DutyAssignmentViewSet.as_view({'post': 'reallocate'}), name='assignment-reallocate'),
    
    # Admin Khidmat Requests
    path('admin/khidmat-requests/', KhidmatRequestAdminListView.as_view(), name='admin-khidmat-requests-list'),
    path('admin/khidmat-requests/<int:pk>/approve/', KhidmatRequestApproveView.as_view(), name='admin-khidmat-requests-approve'),
    path('admin/khidmat-requests/<int:pk>/reject/', KhidmatRequestRejectView.as_view(), name='admin-khidmat-requests-reject'),

    path('', include(router.urls)),
]

"""
API Endpoints:

Registrations:
- GET    /api/registrations/                  - List all registrations
- POST   /api/registrations/                  - Create registration (with files)
- GET    /api/registrations/{id}/             - Get registration details
- GET    /api/registrations/{id}/audition_files/ - Get audition files

Duty Assignments:
- GET    /api/duty-assignments/               - List all assignments
- POST   /api/duty-assignments/               - Assign duty (auto-lock + reminder)
- GET    /api/duty-assignments/{id}/          - Get assignment details
- DELETE /api/duty-assignments/{id}/          - Delete assignment (cancel reminder)
- POST   /api/duty-assignments/{id}/unlock/   - Emergency unlock
- GET    /api/duty-assignments/grid/          - Get Excel-style grid data

Unlock Logs (Read-only):
- GET    /api/unlock-logs/                    - List all unlock logs
- GET    /api/unlock-logs/{id}/               - Get unlock log details

Reminders (Read-only):
- GET    /api/reminders/                      - List all reminders
- GET    /api/reminders/{id}/                 - Get reminder details
- GET    /api/reminders/pending/              - Get pending reminders
- GET    /api/reminders/upcoming/             - Get reminders for next 7 days

Reminder Logs (Read-only):
- GET    /api/reminder-logs/                  - List all reminder logs
- GET    /api/reminder-logs/{id}/             - Get reminder log details
"""
