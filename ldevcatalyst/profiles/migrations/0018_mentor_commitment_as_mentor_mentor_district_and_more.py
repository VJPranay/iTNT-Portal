# Generated by Django 4.2.9 on 2024-06-22 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0017_rename_area_of_intrest_mentor_area_of_interest'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='commitment_as_mentor',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mentor',
            name='district',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mentor',
            name='intensive_mentoring_program',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mentor',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
