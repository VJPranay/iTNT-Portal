# Generated by Django 4.2.9 on 2024-02-16 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0014_startupregistrations_founding_experince_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startupregistrations',
            name='pitch_deck',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='startupregistrations',
            name='video_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
