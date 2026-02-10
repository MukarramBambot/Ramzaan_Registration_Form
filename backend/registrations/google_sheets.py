import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

HEADERS = [
    "Full Name",
    "ITS Number",
    "Email",
    "Contact",
    "Preference",
    "Registered At",
    "Media File",
    "Status"
]

SHEET_NAME = "Registration_Summary"

def ensure_headers(sheet, spreadsheet_id):
    """
    Check if row 1 is empty or missing headers; if so, write headers using RAW mode.
    """
    range_name = f"{SHEET_NAME}!A1:H1"
    logger.error(f"GSYNC-DIAG: [ensure_headers] Checking headers in {range_name}")
    try:
        # 1. Read row 1
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        existing = result.get("values", [])
        logger.error(f"GSYNC-DIAG: [ensure_headers] Current Row 1 values: {existing}")
        
        # 2. Check if row needs headers
        # Conditions: Empty result OR row has no data OR first cell isn't a known header
        needs_headers = False
        if not existing:
            needs_headers = True
        elif not any(str(cell).strip() for cell in existing[0]):
            needs_headers = True
        elif str(existing[0][0]).strip() != "Full Name":
            needs_headers = True
            
        if needs_headers:
            logger.error(f"GSYNC-DIAG: [ensure_headers] Writing headers to {SHEET_NAME}!A1 using RAW mode")
            sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=f"{SHEET_NAME}!A1",
                valueInputOption="RAW",
                body={"values": [HEADERS]}
            ).execute()
            logger.error("GSYNC-DIAG: [ensure_headers] Headers successfully written.")
        else:
            logger.error("GSYNC-DIAG: [ensure_headers] Headers already present. Skipping write.")
            
    except Exception as e:
        logger.error(f"GSYNC-DIAG ERROR: [ensure_headers] Failure: {str(e)}")

def prepare_row_data(registration):
    """
    Constructs a list of values for a single registration row.
    Formats the Media File column as a clickable HYPERLINK.
    """
    # 1. Capture Media Info
    media_file = registration.audition_files.first()
    media_cell = ""
    
    if media_file and media_file.audition_file_path:
        filename = os.path.basename(media_file.audition_file_path.name)
        # Ensure full domain URL
        raw_url = media_file.audition_file_path.url
        site_url = getattr(settings, 'SITE_URL', '').rstrip('/')
        full_url = f"{site_url}{raw_url}" if not raw_url.startswith('http') else raw_url
        
        # Construct formula: =HYPERLINK("url", "label")
        media_cell = f'=HYPERLINK("{full_url}", "{filename}")'
        logger.error(f"GSYNC-DIAG: Constructed HYPERLINK for {registration.its_number}: {media_cell}")
    
    # 2. Assemble Row (Sequential order per requirements)
    return [
        registration.full_name,
        registration.its_number,
        registration.email,
        registration.phone_number,
        registration.get_preference_display(),
        registration.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        media_cell,
        registration.get_status_display()
    ]

def sync_registration_to_sheets(registration):
    """
    Triggers sync for a single new/updated registration.
    """
    logger.error(f"GSYNC-DIAG: [SingleSync] Triggered for ITS: {registration.its_number}")
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        
        creds_path = getattr(settings, 'GOOGLE_SERVICE_ACCOUNT_FILE', None)
        spreadsheet_id = getattr(settings, 'GOOGLE_SHEET_ID', None)

        if not creds_path or not spreadsheet_id or not os.path.exists(creds_path):
            logger.error(f"GSYNC-DIAG ERROR: [SingleSync] Config missing. ID: {spreadsheet_id}, Path: {creds_path}")
            return

        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Phase 1: Header Safety
        ensure_headers(sheet, spreadsheet_id)

        # Phase 2: Data Write
        row_data = prepare_row_data(registration)
        body = {'values': [row_data]}
        append_range = f"{SHEET_NAME}!A2"
        input_option = 'USER_ENTERED'
        
        # MANDATORY DIAGNOSTIC LOG
        media_cell_val = row_data[6]
        logger.error(
            "GSYNC-DIAG: SingleSync media_cell=%r, starts_with_equals=%s, input_mode=%s",
            media_cell_val,
            str(media_cell_val).startswith("="),
            input_option
        )

        logger.error(f"GSYNC-DIAG: [SingleSync] Appending data to {append_range} via {input_option}")
        sheet.values().append(
            spreadsheetId=spreadsheet_id,
            range=append_range,
            valueInputOption=input_option,
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()

        logger.error(f"GSYNC-DIAG SUCCESS: [SingleSync] Record {registration.its_number} appended.")

    except Exception as e:
        logger.error(f"GSYNC-DIAG ERROR: [SingleSync] Execution failed for {registration.its_number}: {str(e)}")

def sync_all_to_sheets():
    """
    Complete refresh of the spreadsheet tab.
    Clears all data, writes headers (RAW), then writes all records (USER_ENTERED).
    """
    logger.error("GSYNC-DIAG: [BulkSync] Initiating full sequence...")
    try:
        from .models import Registration
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        creds_path = getattr(settings, 'GOOGLE_SERVICE_ACCOUNT_FILE', None)
        spreadsheet_id = getattr(settings, 'GOOGLE_SHEET_ID', None)

        if not creds_path or not spreadsheet_id or not os.path.exists(creds_path):
            logger.error(f"GSYNC-DIAG ERROR: [BulkSync] Config missing or invalid. ID: {spreadsheet_id}")
            return False, "Configuration missing"

        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Step 1: Collect Data
        registrations = Registration.objects.all().prefetch_related('audition_files').order_by('created_at')
        count = registrations.count()
        logger.error(f"GSYNC-DIAG: [BulkSync] Loaded {count} registrations for sync.")

        # Step 2: Clean Slate
        clear_range = f"{SHEET_NAME}!A1:Z10000"
        logger.error(f"GSYNC-DIAG: [BulkSync] Clearing range: {clear_range}")
        sheet.values().clear(spreadsheetId=spreadsheet_id, range=clear_range, body={}).execute()

        # Step 3: Write Headers (RAW) at A1
        logger.error(f"GSYNC-DIAG: [BulkSync] Writing headers to {SHEET_NAME}!A1 (RAW mode)")
        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{SHEET_NAME}!A1",
            valueInputOption="RAW",
            body={"values": [HEADERS]}
        ).execute()

        # Step 4: Write Data (USER_ENTERED) starting at A2
        if count > 0:
            data_values = [prepare_row_data(reg) for reg in registrations]
            input_option = 'USER_ENTERED'
            
            # MANDATORY DIAGNOSTIC LOG (for the first row)
            if data_values:
                first_media_cell = data_values[0][6]
                logger.error(
                    "GSYNC-DIAG: BulkSync (Row 1) media_cell=%r, starts_with_equals=%s, input_mode=%s",
                    first_media_cell,
                    str(first_media_cell).startswith("="),
                    input_option
                )

            logger.error(f"GSYNC-DIAG: [BulkSync] Writing {len(data_values)} data rows to {SHEET_NAME}!A2 ({input_option})")
            sheet.values().update(
                spreadsheetId=spreadsheet_id,
                range=f"{SHEET_NAME}!A2",
                valueInputOption=input_option,
                body={"values": data_values}
            ).execute()
        else:
            logger.error("GSYNC-DIAG: [BulkSync] No records found. Skipping data phase.")

        logger.error(f"GSYNC-DIAG SUCCESS: [BulkSync] Full sync completed for {count} records.")
        return True, count

    except Exception as e:
        logger.error(f"GSYNC-DIAG ERROR: [BulkSync] Sequential failure: {str(e)}")
        return False, str(e)
