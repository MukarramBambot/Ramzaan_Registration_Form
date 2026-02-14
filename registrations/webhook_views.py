import json
import logging
from datetime import datetime
import hmac
import hashlib
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from decouple import config
from .models import Registration, Reminder

logger = logging.getLogger(__name__)


def _timestamp_to_datetime(ts):
    try:
        ts_int = int(ts)
    except Exception:
        return None
    # WhatsApp sends seconds since epoch
    # Use datetime.fromtimestamp with UTC tzinfo and return aware datetime
    return datetime.fromtimestamp(ts_int, tz=timezone.utc)


def _verify_signature(request, app_secret):
    header = request.META.get('HTTP_X_HUB_SIGNATURE_256') or request.META.get('HTTP_X_HUB_SIGNATURE')
    if not header:
        return False
    if header.startswith('sha256='):
        signature = header.split('=')[1]
    else:
        signature = header

    computed = hmac.new(app_secret.encode('utf-8'), request.body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, signature)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def whatsapp_webhook(request):
    """Secure WhatsApp Cloud API webhook.

    GET: Verification handshake using `hub.verify_token` compared to env var.
    POST: Accept JSON status updates, validate optional signature, update Registration/Reminder.
    """

    VERIFY_TOKEN = config('WHATSAPP_VERIFY_TOKEN', default=None)
    APP_SECRET = config('WHATSAPP_APP_SECRET', default=None)

    # Verification handshake
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token and token == VERIFY_TOKEN:
            logger.info(json.dumps({'event': 'webhook_verified'}))
            return HttpResponse(challenge or '', status=200)
        logger.warning(json.dumps({'event': 'webhook_verify_failed', 'provided_token': bool(token)}))
        return HttpResponse('Forbidden', status=403)

    # POST: ensure JSON
    content_type = request.META.get('CONTENT_TYPE', '')
    if not content_type.startswith('application/json'):
        logger.warning(json.dumps({'event': 'invalid_content_type', 'content_type': content_type}))
        return HttpResponse('Unsupported Media Type', status=415)

    # Optional signature validation
    if APP_SECRET:
        try:
            valid = _verify_signature(request, APP_SECRET)
        except Exception:
            valid = False
        if not valid:
            logger.warning(json.dumps({'event': 'invalid_signature'}))
            return HttpResponse('Forbidden', status=403)

    try:
        payload = json.loads(request.body)
    except Exception as e:
        logger.error(json.dumps({'event': 'invalid_json', 'error': str(e)}))
        return HttpResponse('Bad Request', status=400)

    # Walk entries safely - WhatsApp may batch multiple entries
    entries = payload.get('entry', []) if isinstance(payload, dict) else []
    for entry in entries:
        changes = entry.get('changes', []) or []
        for change in changes:
            value = change.get('value', {}) or {}
            statuses = value.get('statuses') or []
            for st in statuses:
                try:
                    message_id = st.get('id')
                    recipient_id = st.get('recipient_id')
                    status_raw = (st.get('status') or '').upper()
                    ts = st.get('timestamp')
                    ts_dt = _timestamp_to_datetime(ts)
                    errors = st.get('errors') or st.get('error') or None

                    # Prepare structured log record
                    log_record = {
                        'event': 'whatsapp_status',
                        'message_id': message_id,
                        'recipient_id': recipient_id,
                        'status': status_raw,
                        'timestamp': ts,
                        'errors': errors,
                    }

                    # Update Registration model if present
                    regs = Registration.objects.filter(whatsapp_message_id=message_id)
                    registration_id = None
                    if regs.exists():
                        reg = regs.first()
                        registration_id = reg.id
                        update_kwargs = {'whatsapp_status': status_raw}
                        if status_raw == 'DELIVERED':
                            update_kwargs['whatsapp_delivered_at'] = ts_dt or timezone.now()
                        if status_raw == 'READ':
                            update_kwargs['whatsapp_read_at'] = ts_dt or timezone.now()
                        if status_raw == 'FAILED':
                            # Store both raw error blob and friendly reason
                            update_kwargs['whatsapp_failed_reason'] = json.dumps(errors) if errors else 'Unknown failure'
                            update_kwargs['whatsapp_error'] = json.dumps(errors) if errors else ''
                        regs.update(**update_kwargs)

                    # If not a registration message, update Reminder fallback
                    else:
                        Reminder.objects.filter(whatsapp_message_id=message_id).update(whatsapp_status=status_raw)

                    # Emit structured log
                    log_record['registration_id'] = registration_id
                    logger.info(json.dumps(log_record))

                except Exception as e:
                    logger.error(json.dumps({'event': 'processing_error', 'error': str(e)}))

    # Always acknowledge receipt for Meta to stop retries when processed
    return HttpResponse(status=200)
