from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0019_remove_khidmatrequest_unique_pending_request_per_assignment_and_more'),
    ]

    operations = [
        # 1. DutyAssignment -> Registration
        migrations.RunSQL(
            sql="ALTER TABLE registrations_dutyassignment DROP FOREIGN KEY registrations_dutyas_assigned_user_id_22e62129_fk_registrat;",
            reverse_sql="ALTER TABLE registrations_dutyassignment ADD CONSTRAINT registrations_dutyas_assigned_user_id_22e62129_fk_registrat FOREIGN KEY (assigned_user_id) REFERENCES registrations_registration(id);"
        ),
        migrations.RunSQL(
            sql="ALTER TABLE registrations_dutyassignment ADD CONSTRAINT registrations_dutyas_assigned_user_id_22e62129_fk_registrat FOREIGN KEY (assigned_user_id) REFERENCES registrations_registration(id) ON DELETE CASCADE;",
        ),

        # 2. AuditionFile -> Registration
        migrations.RunSQL(
            sql="ALTER TABLE registrations_auditionfile DROP FOREIGN KEY registrations_auditi_registration_id_f35cca51_fk_registrat;",
            reverse_sql="ALTER TABLE registrations_auditionfile ADD CONSTRAINT registrations_auditi_registration_id_f35cca51_fk_registrat FOREIGN KEY (registration_id) REFERENCES registrations_registration(id);"
        ),
        migrations.RunSQL(
            sql="ALTER TABLE registrations_auditionfile ADD CONSTRAINT registrations_auditi_registration_id_f35cca51_fk_registrat FOREIGN KEY (registration_id) REFERENCES registrations_registration(id) ON DELETE CASCADE;",
        ),

        # 3. KhidmatRequest -> DutyAssignment
        migrations.RunSQL(
            sql="ALTER TABLE registrations_khidmatrequest DROP FOREIGN KEY registrations_khidma_assignment_id_d5b56069_fk_registrat;",
            reverse_sql="ALTER TABLE registrations_khidmatrequest ADD CONSTRAINT registrations_khidma_assignment_id_d5b56069_fk_registrat FOREIGN KEY (assignment_id) REFERENCES registrations_dutyassignment(id);"
        ),
        migrations.RunSQL(
            sql="ALTER TABLE registrations_khidmatrequest ADD CONSTRAINT registrations_khidma_assignment_id_d5b56069_fk_registrat FOREIGN KEY (assignment_id) REFERENCES registrations_dutyassignment(id) ON DELETE CASCADE;",
        ),

        # 4. AssignmentRequestLog -> DutyAssignment
        migrations.RunSQL(
            sql="ALTER TABLE registrations_assignmentrequestlog DROP FOREIGN KEY registrations_assign_duty_assignment_id_816073b8_fk_registrat;",
            reverse_sql="ALTER TABLE registrations_assignmentrequestlog ADD CONSTRAINT registrations_assign_duty_assignment_id_816073b8_fk_registrat FOREIGN KEY (duty_assignment_id) REFERENCES registrations_dutyassignment(id);"
        ),
        migrations.RunSQL(
            sql="ALTER TABLE registrations_assignmentrequestlog ADD CONSTRAINT registrations_assign_duty_assignment_id_816073b8_fk_registrat FOREIGN KEY (duty_assignment_id) REFERENCES registrations_dutyassignment(id) ON DELETE CASCADE;",
        ),

        # 5. Reminder -> DutyAssignment
        migrations.RunSQL(
            sql="ALTER TABLE registrations_reminder DROP FOREIGN KEY registrations_remind_duty_assignment_id_654c3385_fk_registrat;",
            reverse_sql="ALTER TABLE registrations_reminder ADD CONSTRAINT registrations_remind_duty_assignment_id_654c3385_fk_registrat FOREIGN KEY (duty_assignment_id) REFERENCES registrations_dutyassignment(id);"
        ),
        migrations.RunSQL(
            sql="ALTER TABLE registrations_reminder ADD CONSTRAINT registrations_remind_duty_assignment_id_654c3385_fk_registrat FOREIGN KEY (duty_assignment_id) REFERENCES registrations_dutyassignment(id) ON DELETE CASCADE;",
        ),

        # 6. ReminderLog -> Reminder
        migrations.RunSQL(
            sql="ALTER TABLE registrations_reminderlog DROP FOREIGN KEY registrations_remind_reminder_id_9e6cf751_fk_registrat;",
            reverse_sql="ALTER TABLE registrations_reminderlog ADD CONSTRAINT registrations_remind_reminder_id_9e6cf751_fk_registrat FOREIGN KEY (reminder_id) REFERENCES registrations_reminder(id);"
        ),
        migrations.RunSQL(
            sql="ALTER TABLE registrations_reminderlog ADD CONSTRAINT registrations_remind_reminder_id_9e6cf751_fk_registrat FOREIGN KEY (reminder_id) REFERENCES registrations_reminder(id) ON DELETE CASCADE;",
        ),
    ]
