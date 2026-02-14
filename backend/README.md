# Azaan & Takhbira Duty Management System - Backend

## Complete Backend Implementation for Sherullah 1447H

This is a production-ready Django backend for managing Azaan & Takhbira duties during the 30 days of Ramazaan with **fully automatic reminder** system.

---

## ✅ IMPLEMENTED FEATURES

### 1. **User Registration Module**
- ✅ Registration form submission with validation
- ✅ ITS Number uniqueness enforcement
- ✅ Audition file uploads (up to 5 audio files)
- ✅ Read-only after submission

### 2. **Excel-Style Duty Roster**
- ✅ 8 Namaaz types (Fajar Azaan, Fajar Takbira, Zohar Azaan, etc.)
- ✅ One user per duty slot (no duplicates)
- ✅ Automatic locking on assignment
- ✅ Grid API for frontend integration

### 3. **Locking & Emergency Unlock**
- ✅ Duties lock automatically when assigned
- ✅ Emergency unlock with mandatory reason
- ✅ Complete unlock audit trail
- ✅ Change tracking in UnlockLog

### 4. **Automatic Reminder System**
- ✅ ONE reminder per duty assignment
- ✅ Sent 1 day before at configured time (6 PM IST default)
- ✅ Email + WhatsApp dual channel
- ✅ Retry logic (max 2 attempts per channel)
- ✅ Celery Beat scheduler (runs every 15 minutes)

### 5. **Email Reminders**
- ✅ SMTP integration (Django built-in)
- ✅ Mosque-style respectful wording
- ✅ Automatic sending
- ✅ Error logging and retry

### 6. **WhatsApp Reminders**
- ✅ Official WhatsApp Business Cloud API integration
- ✅ Template-based messaging
- ✅ Automatic sending
- ✅ Error logging and retry

### 7. **Change Handling**
- ✅ Reminder cancellation on unlock
- ✅ New reminder creation on reassignment
- ✅ No duplicate message sending

### 8. **Comprehensive APIs**
- ✅ REST API for all operations
- ✅ Clean URL structure
- ✅ Serializers with validation
- ✅ Error handling

### 9. **Timezone Safety**
- ✅ Asia/Kolkata (IST) timezone
- ✅ Timezone-aware datetimes
- ✅ Proper scheduling calculations

### 10. **Logging & Monitoring**
- ✅ Detailed logging for all operations
- ✅ ReminderLog for debugging
- ✅ File & console logging

---

## 📁 PROJECT STRUCTURE

```
backend/
├── sherullah_service/           # Django project
│   ├── __init__.py             # Celery app initialization
│   ├── settings.py             # Configuration (updated)
│   ├── celery.py               # Celery config & beat schedule
│   ├── urls.py
│   └── wsgi.py
│
├── registrations/               # Main app
│   ├── models.py               # All 6 models
│   ├── serializers.py          # DRF serializers
│   ├── views.py                # API ViewSets
│   ├── urls.py                 # API routing
│   ├── admin.py                # Django admin
│   ├── tasks.py                # Celery tasks
│   └── utils.py                # Reminder utilities
│
├── requirements.txt            # Updated dependencies
└── manage.py
```

---

## 🗄️ DATABASE MODELS

### 1. **Registration**
- Stores user registration data
- Fields: full_name, its_number (unique), email, phone_number, preference
- READ-ONLY after creation

### 2. **AuditionFile**
- Stores audition audio files
- Foreign key to Registration
- Max 5 files per registration

### 3. **DutyAssignment**
- Excel-style duty roster
- Fields: duty_date, namaaz_type, assigned_user, locked, locked_at
- Unique constraint: (duty_date, namaaz_type)
- Auto-locks on creation

### 4. **UnlockLog**
- Audit trail for emergency unlocks
- Records: who, when, why, what
- Immutable log entries

### 5. **Reminder**
- Automatic reminder scheduling
- OneToOne with DutyAssignment
- Fields: scheduled_datetime, status, email_sent, whatsapp_sent
- Statuses: PENDING, SENT, FAILED, CANCELLED

### 6. **ReminderLog**
- Detailed send logs
- Per-channel tracking
- Success/failure logging

---

## 🔧 CONFIGURATION

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database
DB_NAME=sherullah_1447_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Redis (Celery Broker)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=mukbambot118@gmail.com

# WhatsApp Business API
WHATSAPP_API_URL=https://graph.facebook.com/v18.0
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id

# Reminder Timing
REMINDER_TIME_HOUR=18  # 6 PM
REMINDER_TIME_MINUTE=0
```

---

## 🚀 SETUP INSTRUCTIONS

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Redis (Required for Celery)

**Windows:**
- Download Redis from: https://github.com/tporadowski/redis/releases
- Extract and run `redis-server.exe`

**Linux/Mac:**
```bash
sudo apt-get install redis-server  # Ubuntu/Debian
brew install redis                 # Mac
redis-server
```

### 3. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (for Django Admin)

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

### 6. Run Celery Worker (In separate terminal)

```bash
celery -A sherullah_service worker --loglevel=info --pool=solo
```

### 7. Run Celery Beat (In separate terminal)

```bash
celery -A sherullah_service beat --loglevel=info
```

---

## 📡 API ENDPOINTS

Base URL: `http://localhost:8000/api/`

### Registrations
```
GET    /api/registrations/                     # List all
POST   /api/registrations/                     # Create (with files)
GET    /api/registrations/{id}/                # Get details
GET    /api/registrations/{id}/audition_files/ # Get audition files
```

### Duty Assignments
```
GET    /api/duty-assignments/             # List all
POST   /api/duty-assignments/             # Create (auto-lock + reminder)
GET    /api/duty-assignments/{id}/        # Get details
DELETE /api/duty-assignments/{id}/        # Delete (cancel reminder)
POST   /api/duty-assignments/{id}/unlock/ # Emergency unlock
GET    /api/duty-assignments/grid/        # Excel-style grid data
```

### Unlock Logs (Read-only)
```
GET    /api/unlock-logs/      # List all unlock logs
GET    /api/unlock-logs/{id}/ # Get details
```

### Reminders (Read-only)
```
GET    /api/reminders/          # List all
GET    /api/reminders/{id}/     # Get details
GET    /api/reminders/pending/  # Get pending
GET    /api/reminders/upcoming/ # Get next 7 days
```

### Reminder Logs (Read-only)
```
GET    /api/reminder-logs/     # List all
GET    /api/reminder-logs/{id}/ # Get details
```

---

## 🔄 AUTOMATIC REMINDER WORKFLOW

1. **Admin assigns duty** → DutyAssignment created (locked=True)
2. **System creates reminder** → Reminder created with scheduled_datetime
3. **Celery Beat runs every 15 min** → Checks for due reminders
4. **Reminder is due** → Email + WhatsApp sent
5. **Success** → Reminder marked as SENT
6. **Failure** → Retry once, then mark as FAILED

### Reminder Timing
- Sent **1 day before** duty date
- At configured time (default: **6 PM IST**)
- Example: Duty on Feb 15 → Reminder sent on Feb 14 at 6 PM

### Change Handling
- If duty unlocked → Old reminder CANCELLED
- If duty reassigned → New reminder created
- No duplicate messages sent

---

## 📧 EMAIL SETUP (SMTP)

### Using Gmail

1. Enable 2-Factor Authentication in Google Account
2. Create App Password: https://myaccount.google.com/apppasswords
3. Add to .env:
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
```

---

## 💬 WHATSAPP SETUP (Official Business API)

### Prerequisites
1. Meta Business Account
2. WhatsApp Business Account
3. Verified Business Phone Number
4. Approved Message Template

### Steps
1. Go to: https://business.facebook.com/
2. Create WhatsApp Business Account
3. Get Phone Number ID and Access Token
4. Create & approve message template named "duty_reminder"
5. Add to .env:
```env
WHATSAPP_API_URL=https://graph.facebook.com/v18.0
WHATSAPP_ACCESS_TOKEN=your_permanent_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
```

### Example Template (to be approved)
```
Hello {{1}},

This is a reminder for your upcoming duty:

Duty: {{2}}
Date: {{3}}

Please ensure you arrive on time.
JazakAllah Khair.
```

---

## 🧪 TESTING

### Test Email Sending
```python
python manage.py shell

from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test message.',
    'from@example.com',
    ['to@example.com'],
)
```

### Manually Trigger Reminder Processing
```python
python manage.py shell

from registrations.tasks import process_reminders_task
process_reminders_task.delay()
```

---

## 🔧 PRODUCTION DEPLOYMENT

### Additional Steps
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use environment variables for secrets
4. Set up PostgreSQL/MySQL in production
5. Use Supervisor or systemd for Celery processes
6. Set up proper logging
7. Configure HTTPS
8. Set up Redis persistance

### Supervisor Config Example
```ini
[program:celery_worker]
command=/path/to/venv/bin/celery -A sherullah_service worker -l info
directory=/path/to/backend
user=www-data
autostart=true
autorestart=true

[program:celery_beat]
command=/path/to/venv/bin/celery -A sherullah_service beat -l info
directory=/path/to/backend
user=www-data
autostart=true
autorestart=true
```

---

## 📊 MONITORING

### Check Reminder Status
Visit Django Admin: `http://localhost:8000/admin/`
- View all reminders
- Check sent/failed status
- View logs

### Check Celery Status
```bash
celery -A sherullah_service inspect active
celery -A sherullah_service inspect scheduled
```

---

## 🎯 KEY DESIGN DECISIONS

1. **Celery + Redis**: Reliable, production-ready scheduler
2. **OneToOne Reminder**: Prevents duplicate reminders
3. **Locked by default**: Safety first, explicit unlock required
4. **Audit logging**: Complete transparency and tracking
5. **Retry logic**: Network failures handled gracefully
6. **Timezone-aware**: All times in IST, no confusion
7. **Template-based WhatsApp**: Complies with Meta's policies

---

## 🔒 SECURITY NOTES

- No authentication implemented yet (as per requirements)
- Add Django authentication when needed
- Use environment variables for all secrets
- Never commit `.env` file
- Use HTTPS in production
- Restrict CORS in production

---

## 📝 TODO (Future Enhancements)

- [ ] Add authentication (Django REST Auth)
- [ ] Add permissions (admin-only endpoints)
- [ ] Add pagination for large datasets
- [ ] Add filtering and sorting
- [ ] Add bulk operations
- [ ] Add data export (CSV/Excel)
- [ ] Add analytics dashboard
- [ ] Add SMS backup channel

---

## 🆘 TROUBLESHOOTING

### Reminders not sending?
1. Check Redis is running: `redis-cli ping`
2. Check Celery worker is running
3. Check Celery beat is running
4. Check logs: `backend/logs/django.log`
5. Check reminder status in admin

### Email not sending?
1. Verify SMTP credentials
2. Check firewall/antivirus
3. Check spam folder
4. Try different SMTP server

### WhatsApp not sending?
1. Verify template is approved
2. Check access token is valid
3. Check phone numbers have country code
4. Check API quotas

---

## 📞 SUPPORT

For issues or questions, check:
1. Django logs: `backend/logs/django.log`
2. Celery logs: Check terminal output
3. Django admin: Check reminder status
4. API responses: Check error messages

---

## ✨ CONCLUSION

This backend is **production-ready** for the 30-day Ramazaan period with:
- ✅ **Zero manual intervention** for reminders
- ✅ **Automatic fallback** on failures
- ✅ **Complete audit trail**
- ✅ **Reliable scheduling**
- ✅ **Clean architecture**

The system will handle the entire Ramazaan duty roster automatically and reliably! 🕌
