# Azaan & Takhbira Duty Management – Sherullah 1447H

A complete web-based system for managing Azaan and Takhbira duties during the 30 days of Ramazaan 1447H (February-March 2026).

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Project Structure](#project-structure)
4. [Frontend Overview](#frontend-overview)
5. [Admin Dashboard Workflow](#admin-dashboard-workflow)
6. [Backend Overview](#backend-overview)
7. [Reminder System](#reminder-system)
8. [WhatsApp Integration](#whatsapp-integration)
9. [Running the Project](#running-the-project)
10. [Important Rules & Constraints](#important-rules--constraints)
11. [Future Enhancements](#future-enhancements)

---

## Project Overview

### What This System Does

This system manages the allocation and notification of Azaan (call to prayer) and Takhbira duties for the 30 days of Ramazaan. It provides:

- A public registration form for community members
- An Excel-style admin dashboard for duty assignment
- Automatic email and WhatsApp reminders sent 1 day before each duty

### Why It Exists

During Ramazaan, mosques need to assign 8 different namaaz duties per day (Fajar Azaan, Fajar Takhbira, Zohar Azaan, etc.) across 30 days. Manual tracking leads to:
- Forgotten reminders
- Assignment conflicts
- Lost audition files
- No audit trail

This system automates the entire process reliably and safely.

### Scope

- **Duration**: 30 days of Ramazaan 1447H only
- **Users**: Mosque administrators and registered community members
- **Scale**: Small (~50-100 registrations, ~240 duty assignments)

### Target Users

1. **Community Members**: Register for duties via simple public form
2. **Mosque Admins**: Assign duties via Excel-style dashboard

---

## Key Features

### User Registration
- Public registration form (no login required)
- Submit name, ITS number, email, WhatsApp number
- Upload audition files (up to 5 audio files)
- Choose preference: Azaan, Takhbira, or Both

### Admin Duty Allotment
- Excel-style grid interface (familiar for admins)
- 30 rows (Ramazaan dates) × 8 columns (namaaz types)
- Click empty cell to assign user
- Searchable dropdown of registered users
- Duties lock automatically after assignment

### Safety Features
- Locked duties cannot be changed accidentally
- Emergency unlock requires mandatory reason (audit trail)
- Complete unlock history log
- No duplicate assignments per slot

### Automatic Reminder System
- Reminders created automatically when duty assigned
- Sent 1 day before duty at 6 PM IST
- Dual channel: Email (free SMTP) + WhatsApp (official API)
- No manual intervention needed
- Handles reassignments (cancels old, creates new)

### UI Philosophy
- Clean, calm, mosque-appropriate design
- Light color palette (no dark mode aggression)
- Excel familiarity for ease of use
- Subtle animations, smooth transitions
- No modern web app complexity

---

## Project Structure

```
sherullah_1447/
│
├── backend/                          # Django backend (REST API + automation)
│   ├── sherullah_service/            # Django project configuration
│   │   ├── settings.py              # Main settings (Celery, email, WhatsApp)
│   │   ├── celery.py                # Celery setup & beat schedule
│   │   └── ...
│   │
│   ├── registrations/                # Main Django app
│   │   ├── models.py                # Database models (6 models)
│   │   ├── views.py                 # REST API endpoints
│   │   ├── serializers.py           # DRF serializers
│   │   ├── utils.py                 # Reminder sending logic
│   │   ├── tasks.py                 # Celery background tasks
│   │   ├── admin.py                 # Django admin interface
│   │   └── ...
│   │
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment variables template
│   ├── README.md                     # Backend-specific documentation
│   └── manage.py                     # Django management script
│
├── sherullah-registration/           # Next.js frontend
│   ├── app/                          # Next.js 13+ app directory
│   │   ├── page.tsx                 # User registration form (public)
│   │   ├── status/page.tsx          # Registration status checker
│   │   └── admin/page.tsx           # Excel-style admin dashboard
│   │
│   ├── public/                       # Static assets
│   ├── package.json                  # Node.js dependencies
│   └── ...
│
├── README.md                         # This file (project overview)
└── start_servers.bat                 # Helper script to start both servers
```

### Folder Purposes

#### `backend/`
Django REST API backend that handles:
- User registration data storage
- Duty assignment logic and locking
- Automatic reminder scheduling (Celery + Redis)
- Email and WhatsApp message sending
- Audit logging

#### `sherullah-registration/`
Next.js frontend that provides:
- Public registration form
- Registration status lookup
- Admin dashboard (Excel-style grid)
- User details panels
- Assignment confirmation dialogs

#### `start_servers.bat`
Convenience script to start both Django and Next.js development servers simultaneously.

---

## Frontend Overview

### Technology Stack

- **Framework**: Next.js 13+ (App Router)
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **Icons**: Lucide React

### Pages

#### 1. Registration Form (`/`)
- Public access (no authentication)
- Form fields: Name, ITS, Email, WhatsApp, Preference
- Audio file upload (drag & drop or select)
- Form validation
- Success confirmation

#### 2. Status Checker (`/status`)
- Look up registration by ITS number
- Shows: Name, Email, Status, Assigned Duties (if any)
- Read-only view

#### 3. Admin Dashboard (`/admin`)
- Excel-style grid (30 dates × 8 duties)
- Empty cells show "–"
- Click to assign user from dropdown
- Locked cells show user name
- Click locked cell to view user details
- Emergency unlock with mandatory reason
- Smooth animations and transitions

### Design Philosophy

The UI is designed to be:
- **Familiar**: Excel-like grid for ease of use
- **Calm**: Light colors, subtle animations
- **Respectful**: Mosque-appropriate, no aggressive design
- **Simple**: No unnecessary complexity
- **Accessible**: Clear states, obvious interactions

### Current Scope

- **No Authentication**: Open access (suitable for trusted admin environment)
- **No Authorization**: Single admin role assumed
- **No API Integration Yet**: Frontend uses local state (backend ready for integration)

---

## Admin Dashboard Workflow

### Step 1: View the Grid

Admin sees an Excel-style table:
- 30 rows: Ramazaan dates (14/02/2026 to 15/03/2026)
- 8 columns: Namaaz duties
- Sticky header and date column
- Empty cells show "–"

### Step 2: Assign a Duty

1. Click an empty cell
2. Searchable dropdown appears with registered users
3. Search by name or ITS number
4. Select a user
5. Confirmation dialog appears
6. Click "Confirm Assignment"
7. Cell updates with user name and locks (visual indicator)
8. Success message: "Duty assigned. Notification will be sent to the user."

### Step 3: View User Details

1. Click a locked cell
2. Side panel slides in from right
3. Shows:
   - Full Name
   - ITS Number
   - Email
   - WhatsApp Number
   - Register For (badges)
   - Audition Audio Player (play/pause)
4. "Emergency Unlock" button at bottom

### Step 4: Emergency Unlock

1. Click "Emergency Unlock" in user details panel
2. Modal appears
3. Enter reason (mandatory, min 10 characters)
4. Click "Confirm Unlock"
5. Unlock is logged (who, when, why)
6. Old reminder is cancelled
7. Cell becomes empty again
8. Admin can now reassign

### Step 5: Visual Feedback

Throughout the workflow:
- Hover effects: Gentle color changes on rows/columns
- Animations: Fade-in for dialogs, slide-in for panels (200-300ms)
- Backdrops: Light blur instead of dark overlays
- Success messages: Brief notification after actions

---

## Backend Overview

### Technology Stack

- **Framework**: Django 5.0
- **API**: Django REST Framework
- **Database**: MySQL
- **Background Tasks**: Celery + Redis
- **Scheduler**: Celery Beat
- **Email**: SMTP (Django built-in)
- **WhatsApp**: Official WhatsApp Business Cloud API

### Core Models

#### 1. Registration
Stores user registration data:
- Full name, ITS number (unique), email, phone number
- Preference (Azaan, Takhbira, Both)
- Created timestamp
- Related audition files

#### 2. AuditionFile
Audio file records:
- Foreign key to Registration
- File path
- Upload timestamp

#### 3. DutyAssignment
Excel-style duty roster:
- Duty date
- Namaaz type (Fajar Azaan, Fajar Takhbira, etc.)
- Assigned user (foreign key)
- Locked flag (default: True)
- Locked timestamp
- Unique constraint: (date, namaaz_type) - prevents duplicates

#### 4. Reminder
Automatic reminder scheduling:
- OneToOne relationship with DutyAssignment
- Scheduled datetime (calculated: duty_date - 1 day, 6 PM IST)
- Email sent flag
- WhatsApp sent flag
- Status (PENDING, SENT, FAILED, CANCELLED)
- Error logging

#### 5. UnlockLog
Audit trail for emergency unlocks:
- Duty assignment reference
- Unlocked timestamp
- Reason (mandatory)
- Unlocked by (admin name)
- Original duty details (for record)

#### 6. ReminderLog
Detailed send logs:
- Reminder reference
- Timestamp
- Channel (EMAIL or WHATSAPP)
- Success flag
- Message/error details

### Locking Logic

When a duty is assigned:
1. DutyAssignment created with `locked=True`
2. Reminder automatically created
3. Cannot be changed without unlock

To change an assignment:
1. Must unlock first (requires reason)
2. UnlockLog is created
3. Old reminder is cancelled
4. Assignment is deleted
5. Admin can now assign someone else
6. New assignment creates new reminder

### API Endpoints

```
POST   /api/registrations/                  # Submit registration
GET    /api/registrations/                  # List all
GET    /api/registrations/{id}/             # Get details

POST   /api/duty-assignments/               # Assign duty (auto-lock + reminder)
GET    /api/duty-assignments/grid/          # Excel-style grid data
POST   /api/duty-assignments/{id}/unlock/   # Emergency unlock
DELETE /api/duty-assignments/{id}/          # Delete

GET    /api/reminders/pending/              # View pending reminders
GET    /api/unlock-logs/                    # View audit trail
```

---

## Reminder System

### How It Works

#### 1. Reminder Creation (Automatic)

When admin assigns a duty:
- System calculates reminder time: `duty_date - 1 day, 6 PM IST`
- Creates Reminder record with status `PENDING`
- OneToOne relationship ensures single reminder per duty

Example:
- Duty assigned: Fajar Azaan on 15/02/2026
- Reminder scheduled: 14/02/2026 at 18:00 IST
- User will receive email + WhatsApp on Feb 14 at 6 PM

#### 2. Reminder Processing (Background Task)

Celery Beat runs every 15 minutes:
1. Finds all reminders with status `PENDING` where `scheduled_datetime <= now`
2. For each reminder:
   - Sends email via SMTP
   - Sends WhatsApp via API
   - Marks flags: `email_sent=True`, `whatsapp_sent=True`
   - Updates status to `SENT`
   - Logs each send in ReminderLog

#### 3. Email Reminder

- **Protocol**: SMTP (Django built-in)
- **Provider**: Gmail (or any SMTP server)
- **Cost**: Free
- **Content**: Respectful mosque-style message
  ```
  Assalamu Alaikum [Name],
  
  This is a reminder for your upcoming duty:
  
  Duty: Fajar Azaan
  Date: Saturday, 15 February 2026
  
  Please ensure you arrive on time.
  May Allah accept your service.
  
  JazakAllah Khair,
  Jamaat Administration
  ```

#### 4. WhatsApp Reminder

- **API**: Official WhatsApp Business Cloud API (Meta)
- **Method**: Template-based messaging (pre-approved)
- **Template Name**: `duty_reminder`
- **Parameters**: User name, duty type, date
- **Cost**: Very low (utility category pricing)
- **Compliance**: Official, safe, spam-free

#### 5. Retry Logic

If sending fails:
- System retries once (max 2 attempts per channel)
- Logs error in `last_error` field
- If both attempts fail, status = `FAILED`

#### 6. Reminder Cancellation

When duty is unlocked or reassigned:
- Old reminder status set to `CANCELLED`
- No message sent
- New reminder created for new assignment (if any)

### No Duplicate Messages Guarantee

- OneToOne relationship (1 reminder per duty)
- Status tracking prevents re-sending
- Cancelled reminders are skipped
- Idempotent processing

### Volume

For 30 days × 8 duties = 240 assignments:
- Total reminders: 240
- Per day: ~8-9 messages
- Very low volume (well within WhatsApp Business limits)

---

## WhatsApp Integration

### Official WhatsApp Business API

This system uses the **Official WhatsApp Business Cloud API** provided by Meta (Facebook). This is NOT a third-party bot or unofficial solution.

### Why Official API?

1. **Compliant**: Follows WhatsApp's terms of service
2. **Reliable**: Enterprise-grade delivery
3. **Safe**: No risk of account suspension
4. **Professional**: Sent from verified business number
5. **Low Cost**: Utility messages are very affordable

### How It Works

#### Setup (One-time)
1. Create Meta Business Account
2. Set up WhatsApp Business Account
3. Verify business phone number
4. Create message template (submit for approval)
5. Get access token and phone number ID

#### Template-Based Messaging
WhatsApp requires pre-approved templates for automated messages. Our template:

**Template Name**: `duty_reminder`

**Category**: Utility (lowest cost tier)

**Template Body**:
```
Hello {{1}},

This is a reminder for your upcoming duty:

Duty: {{2}}
Date: {{3}}

Please ensure you arrive on time.
JazakAllah Khair.
```

**Parameters**:
1. User's name
2. Duty type (e.g., "Fajar Azaan")
3. Duty date (e.g., "15/02/2026")

#### Message Sending
The backend automatically:
1. Formats the template with user-specific data
2. Sends HTTP POST to WhatsApp API
3. Receives delivery confirmation
4. Logs success/failure

### Cost

- **Utility messages**: Very low cost per message
- **Volume**: ~240 messages for entire Ramazaan
- **Total estimated cost**: Minimal (a few dollars)

### Compliance

- Uses official API (no bots, no scraping)
- Template pre-approved by Meta
- Low frequency (1 message per user per duty)
- Opt-in via registration (users provide WhatsApp number)

---

## Running the Project

### Prerequisites

1. **Node.js** (v18 or higher) for frontend
2. **Python 3.10+** for backend
3. **MySQL** database server
4. **Redis** server (for Celery)
5. **SMTP access** (e.g., Gmail with app password)
6. **WhatsApp Business API** credentials (optional for testing)

### Quick Start

#### Backend Setup

1. Navigate to `backend/` directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` file (copy from `.env.example`)
4. Configure database, email, WhatsApp credentials
5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```
7. Start Django server:
   ```bash
   python manage.py runserver
   ```
8. Start Celery worker (separate terminal):
   ```bash
   celery -A sherullah_service worker --loglevel=info --pool=solo
   ```
9. Start Celery beat (separate terminal):
   ```bash
   celery -A sherullah_service beat --loglevel=info
   ```

#### Frontend Setup

1. Navigate to `sherullah-registration/` directory
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start development server:
   ```bash
   npm run dev
   ```
4. Access at `http://localhost:3000`

### Environment Variables

Backend requires (`.env` file):
- Database credentials (MySQL)
- Redis URL
- SMTP settings (email)
- WhatsApp API credentials
- Reminder timing configuration

See `backend/.env.example` for full template.

### Directory-Specific Documentation

- **Backend details**: See `backend/README.md`
- **API documentation**: See `backend/README.md` (API Endpoints section)
- **Frontend details**: Component-level documentation in source files

---

## Important Rules & Constraints

### Duty Assignment Rules

1. **Once assigned, duties are locked**: Prevents accidental changes
2. **Emergency unlock requires reason**: Mandatory 10+ character explanation
3. **No duplicate assignments**: Unique constraint on (date, namaaz_type)
4. **Single user per duty slot**: One person cannot be assigned to same slot twice

### Reminder Rules

1. **One reminder per duty**: OneToOne relationship enforced
2. **Sent 1 day before at 6 PM IST**: Fixed timing, configurable
3. **No duplicate messages**: Status tracking prevents re-sending
4. **Auto-cancellation on unlock**: Old reminders cancelled when duty changes
5. **No manual reminders**: All reminders created automatically

### Data Integrity

1. **No dummy data in production**: Admin dashboard starts clean
2. **Registration is read-only**: Cannot be edited after submission
3. **Audit logs are immutable**: UnlockLog cannot be modified
4. **ITS numbers are unique**: Prevents duplicate registrations

### Timezone

1. **Fixed timezone**: Asia/Kolkata (IST) throughout
2. **No timezone confusion**: All dates/times in IST
3. **No UTC conversion issues**: System enforces single timezone

### Scope Limitation

1. **Ramazaan-only**: Designed for 30-day period
2. **Single mosque**: No multi-mosque support (currently)
3. **No authentication**: Suitable for trusted admin environment
4. **No user portal**: Members cannot view their own assignments

### Technical Constraints

1. **Excel-style interface**: Grid must remain familiar
2. **Light UI theme**: No dark mode for mosque setting
3. **Template-based WhatsApp**: Messages must use approved templates
4. **Celery required**: Background tasks need Redis + Celery

---

## Future Enhancements

The following features may be added in future versions:

### Authentication & Authorization
- Admin login system
- Role-based permissions (super admin, duty admin, viewer)
- User portal for viewing own assignments

### Multi-Mosque Support
- Multiple mosque branches in single system
- Per-mosque admin dashboards
- Shared user pool

### Extended Functionality
- SMS reminder backup channel
- PDF export of complete duty roster
- Analytics dashboard (assignment statistics)
- Mobile app for admins

### User Experience
- Mobile-responsive admin dashboard
- Assignment history timeline
- Bulk assignment tools
- Calendar view option

**Note**: These are potential enhancements only. Current version is focused on core functionality for a single mosque during Ramazaan 1447H.

---

## Support & Maintenance

### Logs

- **Django logs**: `backend/logs/django.log`
- **Celery output**: Console output from worker/beat terminals
- **Reminder logs**: Database table `registrations_reminderlog`
- **Unlock logs**: Database table `registrations_unlocklog`

### Common Issues

**Reminders not sending?**
1. Check Redis is running
2. Check Celery worker is running
3. Check Celery beat is running
4. Check SMTP/WhatsApp credentials
5. Review logs for errors

**Assignment conflicts?**
- Database constraint prevents duplicate assignments
- If error occurs, duty slot is already taken

**UI not updating?**
- Frontend currently uses local state
- Backend integration will require API calls

### Technical Documentation

For detailed technical documentation:
- Backend architecture: `backend/ARCHITECTURE.md`
- Backend setup: `backend/README.md`
- Backend implementation: `backend/IMPLEMENTATION_SUMMARY.md`

---

## License

This project was developed for the Dawoodi Bohra community for managing mosque duties during Ramazaan 1447H.

---

## Acknowledgments

Built with the intention of serving the community during the blessed month of Ramazaan. May Allah accept this service and make it beneficial for all.

---

**Last Updated**: February 2026  
**Version**: 1.0.0  
**Ramazaan Period**: Sherullah 1447H (February-March 2026)
