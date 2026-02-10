import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def sync_registration_to_sheets(registration):
    """
    Sync a single registration to Google Sheets as a new row.
    """
    try:
        # Lazy imports to prevent startup crashes if dependencies are missing
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        # Load credentials
        creds_path = getattr(settings, 'GOOGLE_SERVICE_ACCOUNT_FILE', None)
        spreadsheet_id = getattr(settings, 'GOOGLE_SHEET_ID', None)

        if not creds_path or not spreadsheet_id:
            logger.warning("Google Sheets credentials or Spreadsheet ID not configured. Skipping sync.")
            return

        if not os.path.exists(creds_path):
            logger.error(f"Google service account file not found at {creds_path}")
            return

        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)

        # Prepare row data
        # Columns: Full Name, ITS Number, Email Address, WhatsApp Number, Register For, Registration Date, Audition File
        files = registration.audition_files.all()
        file_urls = ", ".join([f"{settings.SITE_URL}{f.audition_file_path.url}" if hasattr(settings, 'SITE_URL') else f.audition_file_path.url for f in files])
        
        row_data = [
            registration.full_name,
            registration.its_number,
            registration.email,
            registration.phone_number,
            registration.get_preference_display(),
            registration.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            file_urls
        ]

        # Append to sheet
        sheet = service.spreadsheets()
        body = {
            'values': [row_data]
        }
        
        result = sheet.values().append(
            spreadsheetId=spreadsheet_id,
            range='A2',  # Assuming header is row 1
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()

        logger.info(f"Successfully synced registration {registration.its_number} to Google Sheets: {result.get('updates').get('updatedCells')} cells updated.")

    except Exception as e:
        logger.error(f"Failed to sync registration to Google Sheets: {str(e)}")

def sync_all_to_sheets():
    """
    Clear existing data and sync all registrations to Google Sheets.
    """
    try:
        from .models import Registration
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        creds_path = getattr(settings, 'GOOGLE_SERVICE_ACCOUNT_FILE', None)
        spreadsheet_id = getattr(settings, 'GOOGLE_SHEET_ID', None)

        if not creds_path or not spreadsheet_id or not os.path.exists(creds_path):
            logger.error("Sync All failed: Google Sheets configuration error or missing creds file.")
            return False

        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Fetch all registrations with audition files
        registrations = Registration.objects.all().prefetch_related('audition_files').order_by('created_at')
        
        values = []
        for reg in registrations:
            files = reg.audition_files.all()
            file_urls = ", ".join([f"{settings.SITE_URL}{f.audition_file_path.url}" if hasattr(settings, 'SITE_URL') else f.audition_file_path.url for f in files])
            
            values.append([
                reg.full_name,
                reg.its_number,
                reg.email,
                reg.phone_number,
                reg.get_preference_display(),
                reg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                file_urls
            ])

        if not values:
            logger.info("Sync All: No registrations to sync.")
            return True

        # Clear existing data (A2:G1000)
        sheet.values().clear(
            spreadsheetId=spreadsheet_id,
            range='A2:G1000',
            body={}
        ).execute()

        # Update with new values
        body = {'values': values}
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range='A2',
            valueInputOption='RAW',
            body=body
        ).execute()

        logger.info(f"Successfully bulk synced {len(values)} registrations to Google Sheets.")
        return True

    except Exception as e:
        logger.error(f"Bulk sync to Google Sheets failed: {str(e)}")
        return False
