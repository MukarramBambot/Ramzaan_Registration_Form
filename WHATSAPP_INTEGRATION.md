# WhatsApp Cloud API Integration Guide

## Overview

This Django backend is integrated with **WhatsApp Cloud API** (Meta Graph API) to send automated template messages for:

1. **Registration Confirmation** - When a user submits the registration form
2. **Duty Allotment Notification** - When admin assigns duty to a user
3. **Duty Reminder** - One day before the duty date

---

## Configuration

### Environment Variables

Add the following to your `.env` file:

```bash
# WhatsApp (Meta WhatsApp Cloud API)
WHATSAPP_PROVIDER=meta
META_WA_PHONE_NUMBER_ID=your_phone_number_id
META_WA_ACCESS_TOKEN=your_permanent_access_token
META_WA_BUSINESS_ACCOUNT_ID=your_business_account_id
META_WA_API_VERSION=v18.0
```

### Django Settings

The settings are automatically loaded in `sherullah_service/settings.py`:

```python
META_WA_PHONE_NUMBER_ID = os.getenv("META_WA_PHONE_NUMBER_ID")
META_WA_ACCESS_TOKEN = os.getenv("META_WA_ACCESS_TOKEN")
META_WA_BUSINESS_ACCOUNT_ID = os.getenv("META_WA_BUSINESS_ACCOUNT_ID")
META_WA_API_VERSION = os.getenv("META_WA_API_VERSION", "v18.0")
```

---

## Template Messages

### 1. `registration_received`
**Trigger**: When user submits registration form  
**Parameters**:
- `{{1}}` = Full Name

**Example**:
```
Hello Ahmed Ali,
Your registration has been received successfully.
```

### 2. `duty_allotment_confirmed`
**Trigger**: When admin assigns duty to a user  
**Parameters**:
- `{{1}}` = Full Name
- `{{2}}` = Duty Date (e.g., "15 March 2026")
- `{{3}}` = Duty Time (e.g., "Fajar Azaan")

**Example**:
```
Assalamu Alaikum Ahmed Ali,
You have been assigned duty on 15 March 2026 for Fajar Azaan.
```

### 3. `duty_reminder_tomorrow`
**Trigger**: One day before duty date (scheduled via Celery)  
**Parameters**:
- `{{1}}` = Full Name
- `{{2}}` = Duty Date
- `{{3}}` = Duty Time

**Example**:
```
Reminder: Ahmed Ali, your duty is tomorrow on 15 March 2026 for Fajar Azaan.
```

---

## Core Function

### `send_whatsapp_template(template_name, phone_number, parameters)`

**Location**: `registrations/utils/whatsapp.py`

**Usage**:
```python
from registrations.utils.whatsapp import send_whatsapp_template

# Example: Send registration confirmation
send_whatsapp_template(
    template_name="registration_received",
    phone_number="919876543210",
    parameters=["Ahmed Ali"]
)

# Example: Send duty allotment
send_whatsapp_template(
    template_name="duty_allotment_confirmed",
    phone_number="919876543210",
    parameters=["Ahmed Ali", "15 March 2026", "Fajar Azaan"]
)
```

**Parameters**:
- `template_name` (str): Name of the approved WhatsApp template
- `phone_number` (str): Recipient phone number (with country code)
- `parameters` (list): List of strings for template variables `{{1}}`, `{{2}}`, etc.

**Returns**: `bool` - `True` if successful, `False` otherwise

---

## Integration Points

### 1. Registration Form Submission

**File**: `registrations/signals.py`

When a new registration is created, the `registration_post_save` signal automatically triggers:

```python
@receiver(post_save, sender=Registration)
def registration_post_save(sender, instance, created, **kwargs):
    if created:
        safe_task_delay(send_registration_confirmation_task, instance.id, non_blocking=True)
```

**Task**: `registrations/tasks.py` → `send_registration_confirmation_task`

This task calls:
```python
from registrations.utils.whatsapp import send_registration_notification
send_registration_notification(registration)
```

### 2. Duty Allotment

**File**: `registrations/signals.py`

When a duty assignment is created, the `duty_assignment_post_save` signal triggers:

```python
@receiver(post_save, sender=DutyAssignment)
def duty_assignment_post_save(sender, instance, created, **kwargs):
    if created:
        safe_task_delay(send_duty_allotment_notification_task, instance.id, non_blocking=True)
```

**Task**: `registrations/tasks.py` → `send_duty_allotment_notification_task`

This task calls:
```python
from registrations.utils.whatsapp import send_duty_allotment_notification
send_duty_allotment_notification(duty_assignment)
```

### 3. Duty Reminders (One Day Before)

**Celery Task**: `registrations/tasks.py` → `process_reminders_task`

This task runs periodically (every 15 minutes recommended) and processes pending reminders.

**Celery Beat Configuration**:
```bash
# In Django admin or via code
from django_celery_beat.models import PeriodicTask, IntervalSchedule

schedule, _ = IntervalSchedule.objects.get_or_create(
    every=15,
    period=IntervalSchedule.MINUTES,
)

PeriodicTask.objects.create(
    interval=schedule,
    name='Process Reminders',
    task='registrations.process_reminders',
)
```

**Manual Command**:
```bash
python manage.py send_reminders
```

---

## API Endpoint

**URL**: `https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages`  
**Method**: `POST`  
**Headers**:
```json
{
  "Authorization": "Bearer {ACCESS_TOKEN}",
  "Content-Type": "application/json"
}
```

**Payload Example**:
```json
{
  "messaging_product": "whatsapp",
  "to": "919876543210",
  "type": "template",
  "template": {
    "name": "registration_received",
    "language": {
      "code": "en"
    },
    "components": [
      {
        "type": "body",
        "parameters": [
          {"type": "text", "text": "Ahmed Ali"}
        ]
      }
    ]
  }
}
```

---

## Testing

### Test Payload Structure

Run the test script to verify payload structure:

```bash
cd /var/www/Ramzaan_Registration_Form/backend
python test_whatsapp_payloads.py
```

### Test Registration Flow

1. Submit a registration via API
2. Check logs: `tail -f logs/django.log`
3. Look for: `[WhatsApp] Sending template 'registration_received' to ...`

### Test Duty Allotment

1. Create a duty assignment in Django admin
2. Check logs for: `[WhatsApp] Sending template 'duty_allotment_confirmed' to ...`

### Test Reminders

```bash
python manage.py send_reminders
```

---

## Error Handling

All WhatsApp functions include:
- **Logging**: All requests/responses logged to `logs/django.log`
- **Retry Logic**: Celery tasks retry up to 3 times on failure
- **Idempotency**: Flags (`whatsapp_sent`, `allotment_notification_sent`) prevent duplicate messages
- **Graceful Degradation**: Email notifications continue even if WhatsApp fails

---

## Production Checklist

- [x] Meta App created and published
- [x] WhatsApp Cloud API enabled
- [x] Phone number registered
- [x] Permanent access token generated
- [x] Templates created and approved:
  - `registration_received`
  - `duty_allotment_confirmed`
  - `duty_reminder_tomorrow`
- [x] Environment variables configured in `.env`
- [x] Celery worker running: `sudo systemctl status celery`
- [x] Celery beat running: `sudo systemctl status celerybeat`
- [x] Redis running: `sudo systemctl status redis`

---

## Logs

Monitor WhatsApp API calls:

```bash
tail -f /var/www/Ramzaan_Registration_Form/backend/logs/django.log | grep WhatsApp
```

---

## Support

For Meta Graph API documentation:
- [WhatsApp Cloud API Docs](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Template Messages Guide](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates)
