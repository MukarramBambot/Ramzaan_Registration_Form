from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0012_alter_registration_preference'),
    ]

    operations = [
        migrations.AddField(
            model_name='dutyassignment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancel_requested', 'Cancel Requested'), ('reallocation_requested', 'Reallocation Requested'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', help_text='Extended lifecycle state for this assignment', max_length=50),
        ),
        migrations.AddField(
            model_name='dutyassignment',
            name='cancel_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dutyassignment',
            name='reallocation_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dutyassignment',
            name='reallocation_requested_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dutyassignment',
            name='cancel_requested_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='AssignmentRequestLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(choices=[('cancel', 'Cancel Request'), ('reallocate', 'Reallocation Request')], max_length=20)),
                ('requested_by_its', models.CharField(max_length=20)),
                ('reason', models.TextField(blank=True, null=True)),
                ('preferred_datetime', models.CharField(blank=True, null=True, max_length=255)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField(default=False)),
                ('duty_assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_logs', to='registrations.dutyassignment')),
            ],
            options={'ordering': ['-requested_at']},
        ),
    ]
