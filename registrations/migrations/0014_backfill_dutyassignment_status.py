from django.db import migrations


def forwards(apps, schema_editor):
    DutyAssignment = apps.get_model('registrations', 'DutyAssignment')
    # Mark existing locked assignments as confirmed (safe, non-destructive)
    DutyAssignment.objects.filter(status='pending', locked=True).update(status='confirmed')


def backwards(apps, schema_editor):
    DutyAssignment = apps.get_model('registrations', 'DutyAssignment')
    # Revert only those we changed above back to pending
    DutyAssignment.objects.filter(status='confirmed', locked=True).update(status='pending')


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0013_add_assignment_request_fields'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
