"""
Google Sheets sync for Vajebaat appointments.
Writes to a separate tab 'Vajebaat_1447' in the same spreadsheet.
Does NOT touch the registrations 'Registration_Summary' tab.
"""

import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

SHEET_NAME = "Vajebaat_1447"

HEADERS = [
    "ITS",
    "Name",
    "Mobile",
    "Preferred Date",
    "Assigned Date",
    "Slot Time",
    "Status",
    "Confirmed At",
    "Created At",
]


def _get_sheets_service():
    """Build and return Google Sheets API service, or None if unconfigured."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds_path = getattr(settings, 'GOOGLE_SERVICE_ACCOUNT_FILE', None)
    spreadsheet_id = getattr(settings, 'GOOGLE_SHEET_ID', None)

    if not creds_path or not spreadsheet_id:
        logger.warning("Vajebaat GSheets: config missing (creds_path=%s, sheet_id=%s)", creds_path, spreadsheet_id)
        return None, None

    if not os.path.exists(creds_path):
        logger.warning("Vajebaat GSheets: credentials file not found at %s", creds_path)
        return None, None

    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets(), spreadsheet_id


def _ensure_tab_exists(sheet, spreadsheet_id):
    """Create the Vajebaat_1447 tab if it doesn't exist yet."""
    try:
        meta = sheet.get(spreadsheetId=spreadsheet_id).execute()
        existing_tabs = [s['properties']['title'] for s in meta.get('sheets', [])]
        if SHEET_NAME not in existing_tabs:
            body = {
                'requests': [{
                    'addSheet': {
                        'properties': {'title': SHEET_NAME}
                    }
                }]
            }
            sheet.batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
            logger.info("Vajebaat GSheets: created tab '%s'", SHEET_NAME)
    except Exception as e:
        logger.error("Vajebaat GSheets: failed to ensure tab: %s", e)


def _prepare_row(appointment):
    """Convert a VajebaatAppointment into a flat row list."""
    assigned_date = ""
    slot_time = ""

    if appointment.slot:
        slot = appointment.slot
        if slot.date:
            assigned_date = str(slot.date.date)
        slot_time = (
            f"{slot.start_time.strftime('%H:%M')} – "
            f"{slot.end_time.strftime('%H:%M')}"
        )

    return [
        appointment.its_number,
        appointment.name,
        appointment.mobile or "",
        str(appointment.preferred_date) if appointment.preferred_date else "",
        assigned_date,
        slot_time,
        appointment.status,
        appointment.confirmed_at.strftime('%Y-%m-%d %H:%M') if appointment.confirmed_at else "",
        appointment.created_at.strftime('%Y-%m-%d %H:%M') if appointment.created_at else "",
    ]


def sync_vajebaat_members():
    """
    Full sync: clear tab, write headers + all appointment data.
    Returns (success: bool, detail: str|int).

    NOTE: This does a full clear + rewrite on every call. For MVP this is
    acceptable, but with 500+ records consider incremental row updates
    (find row by ITS, update in place) to reduce API quota usage.
    """
    from .models import VajebaatAppointment

    sheet, spreadsheet_id = _get_sheets_service()
    if not sheet:
        return False, "Google Sheets not configured"

    try:
        _ensure_tab_exists(sheet, spreadsheet_id)

        appointments = (
            VajebaatAppointment.objects
            .select_related('slot', 'slot__date')
            .order_by('created_at')
        )
        count = appointments.count()

        # Clear existing data
        clear_range = f"{SHEET_NAME}!A1:Z10000"
        sheet.values().clear(
            spreadsheetId=spreadsheet_id,
            range=clear_range,
            body={}
        ).execute()

        # Write headers (RAW)
        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{SHEET_NAME}!A1",
            valueInputOption="RAW",
            body={"values": [HEADERS]}
        ).execute()

        # Write data rows
        if count > 0:
            rows = [_prepare_row(apt) for apt in appointments]
            sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=f"{SHEET_NAME}!A2",
                valueInputOption="USER_ENTERED",
                body={"values": rows}
            ).execute()

        logger.info("Vajebaat GSheets: synced %d records to '%s'", count, SHEET_NAME)
        return True, count

    except Exception as e:
        logger.error("Vajebaat GSheets: sync failed: %s", e)
        return False, str(e)
