"""
URL routing for Vajebaat API endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VajebaatMemberViewSet,
    VajebaatFormViewSet,
    VajebaatAppointmentViewSet,
    VajebaatDateViewSet,
    VajebaatSlotViewSet,
    dashboard_stats,
    members_directory,
    sync_vajebaat_sheet,
    export_csv,
)

router = DefaultRouter()
router.register(r'members', VajebaatMemberViewSet, basename='vajebaat-member')
router.register(r'forms', VajebaatFormViewSet, basename='vajebaat-form')
router.register(r'appointments', VajebaatAppointmentViewSet, basename='vajebaat-appointment')
router.register(r'dates', VajebaatDateViewSet, basename='vajebaat-date')
router.register(r'slots', VajebaatSlotViewSet, basename='vajebaat-slot')

urlpatterns = [
    path('dashboard-stats/', dashboard_stats, name='vajebaat-dashboard-stats'),
    path('members-directory/', members_directory, name='vajebaat-members-directory'),
    path('sync-sheet/', sync_vajebaat_sheet, name='vajebaat-sync-sheet'),
    path('export-csv/', export_csv, name='vajebaat-export-csv'),
    path('', include(router.urls)),
]

"""
API Endpoints:

Members:
- GET    /api/vajebaat/members/                  - List all members (Admin)
- POST   /api/vajebaat/members/                  - Create member (Admin)
- GET    /api/vajebaat/members/{id}/             - Get member details (Admin)
- GET    /api/vajebaat/members/by_its/?its=X     - Lookup by ITS (Public)

Forms (Takhmeen):
- GET    /api/vajebaat/forms/                    - List all forms (Admin)
- POST   /api/vajebaat/forms/                    - Submit form (Public)
- GET    /api/vajebaat/forms/{id}/               - Get form details (Admin)

Appointments:
- GET    /api/vajebaat/appointments/                         - List all (Admin)
- POST   /api/vajebaat/appointments/                         - Book appointment (Public)
- GET    /api/vajebaat/appointments/{id}/                    - Get details (Admin)
- PATCH  /api/vajebaat/appointments/{id}/update_status/      - Update status (Admin)
- POST   /api/vajebaat/appointments/{id}/assign-slot/        - Assign slot (Admin)
- PATCH  /api/vajebaat/appointments/{id}/reschedule/         - Reschedule slot (Admin)
- PATCH  /api/vajebaat/appointments/{id}/cancel/             - Cancel appointment (Admin)

Dates:
- GET    /api/vajebaat/dates/                    - List all dates (Admin)
- GET    /api/vajebaat/dates/{id}/               - Get date detail (Admin)

Slots:
- GET    /api/vajebaat/slots/                    - List all slots (Admin)
- GET    /api/vajebaat/slots/?date_id=X          - Filter by date (Admin)
- GET    /api/vajebaat/slots/{id}/               - Get slot detail (Admin)

Dashboard:
- GET    /api/vajebaat/dashboard-stats/          - Admin metrics

Members Directory:
- GET    /api/vajebaat/members-directory/         - Paginated directory (Admin)

Google Sheets:
- POST   /api/vajebaat/sync-sheet/               - Manual sync (Admin)

Export:
- GET    /api/vajebaat/export-csv/                - Download CSV (Admin)
"""
