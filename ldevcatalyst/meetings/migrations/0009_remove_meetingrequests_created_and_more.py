# Generated by Django 4.2.9 on 2024-05-20 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0008_alter_meetingrequests_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetingrequests',
            name='created',
        ),
        migrations.RemoveField(
            model_name='meetingrequests',
            name='meeting_date',
        ),
        migrations.RemoveField(
            model_name='meetingrequests',
            name='meeting_date_time',
        ),
        migrations.RemoveField(
            model_name='meetingrequests',
            name='meeting_location',
        ),
        migrations.RemoveField(
            model_name='meetingrequests',
            name='meeting_time',
        ),
        migrations.RemoveField(
            model_name='meetingrequests',
            name='meeting_type',
        ),
        migrations.RemoveField(
            model_name='meetingrequests',
            name='message',
        ),
        migrations.RemoveField(
            model_name='meetingrequests',
            name='next_level',
        ),
        migrations.RemoveField(
            model_name='meetingrequests',
            name='start_up',
        ),
        migrations.RemoveField(
            model_name='meetingrequests',
            name='status',
        ),
        migrations.RemoveField(
            model_name='meetingrequests',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='meetingrequests',
            name='vc',
        ),
    ]
