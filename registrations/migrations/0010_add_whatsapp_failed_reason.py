from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0009_registration_whatsapp_delivered_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='whatsapp_failed_reason',
            field=models.TextField(blank=True, null=True, help_text='Human-readable failure reason from WhatsApp'),
        ),
    ]
