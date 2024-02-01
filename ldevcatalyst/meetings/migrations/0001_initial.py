# Generated by Django 4.2.9 on 2024-02-01 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0005_startup_short_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected')], max_length=50, null=True)),
                ('start_up', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.startup')),
                ('vc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.vc')),
            ],
        ),
    ]