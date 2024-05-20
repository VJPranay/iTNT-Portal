# Generated by Django 4.2.9 on 2024-05-20 04:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_vc_name'),
        ('meetings', '0009_remove_meetingrequests_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingrequests',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetingrequests',
            name='meeting_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meetingrequests',
            name='meeting_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meetingrequests',
            name='meeting_location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meetingrequests',
            name='meeting_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meetingrequests',
            name='meeting_type',
            field=models.CharField(blank=True, choices=[('online', 'online'), ('offline', 'offline')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='meetingrequests',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meetingrequests',
            name='next_level',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='meetingrequests',
            name='start_up',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.startup'),
        ),
        migrations.AddField(
            model_name='meetingrequests',
            name='status',
            field=models.CharField(blank=True, choices=[('start_up_request', 'start_up_request'), ('vc_accepted', 'vc_accepted'), ('scheduled', 'scheduled'), ('online_meeting_link_awaiting', 'online_meeting_link_awaiting'), ('start_up_reschedule', 'start_up_reschedule'), ('rejected', 'rejected')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='meetingrequests',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='meetingrequests',
            name='vc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.vc'),
        ),
    ]
