# Generated by Django 4.2.9 on 2024-06-01 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smeconnect', '0002_alter_meetingrequest_meeting_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meetingrequest',
            old_name='meeting_link',
            new_name='meeting_details',
        ),
    ]
