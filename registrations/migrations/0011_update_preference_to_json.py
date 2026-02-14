from django.db import migrations, models
import re


def forwards(apps, schema_editor):
    Registration = apps.get_model('registrations', 'Registration')
    for reg in Registration.objects.all():
        pref = getattr(reg, 'preference', None)
        try:
            if pref is None:
                reg.preference_list = []
            else:
                s = str(pref).strip()
                up = s.upper()
                # Known legacy codes
                if up == 'AZAAN':
                    reg.preference_list = ['Azaan']
                elif up == 'TAKHBIRA':
                    reg.preference_list = ['Takhbira']
                elif up == 'BOTH':
                    reg.preference_list = ['Azaan', 'Takhbira']
                else:
                    # Specific legacy string mapping: map Sanah compound label to 'Sanah'
                    low = s.lower()
                    if 'sanah' in low or 'shayweed' in low or 'jayweed' in low or 'majid' in low:
                        reg.preference_list = ['Sanah']
                    else:
                        parts = [p.strip().title() for p in re.split(r'[,&/\\\\|]+', s) if p.strip()]
                        reg.preference_list = parts or [s]
            reg.save(update_fields=['preference_list'])
        except Exception:
            # If any row fails, skip to avoid migration crash; preserve original value in DB.
            continue


def backwards(apps, schema_editor):
    Registration = apps.get_model('registrations', 'Registration')
    for reg in Registration.objects.all():
        plist = getattr(reg, 'preference_list', None)
        if not plist:
            reg.preference = ''
        else:
            # Try to map known lists back to legacy codes
            up = [p.strip().upper() for p in plist]
            if up == ['AZAAN']:
                reg.preference = 'AZAAN'
            elif up == ['TAKHBIRA']:
                reg.preference = 'TAKHBIRA'
            elif set(up) == set(['AZAAN', 'TAKHBIRA']):
                reg.preference = 'BOTH'
            else:
                reg.preference = ','.join(plist)
        reg.save(update_fields=['preference'])


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0010_add_whatsapp_failed_reason'),
    ]

    operations = [
        # 1) Add temporary JSON field to hold lists
        migrations.AddField(
            model_name='registration',
            name='preference_list',
            field=models.JSONField(default=list, null=True),
        ),
        # 2) Populate preference_list from existing preference values
        migrations.RunPython(forwards, backwards),
        # 3) Remove old char-based preference
        migrations.RemoveField(
            model_name='registration',
            name='preference',
        ),
        # 4) Rename new field to 'preference'
        migrations.RenameField(
            model_name='registration',
            old_name='preference_list',
            new_name='preference',
        ),
    ]
