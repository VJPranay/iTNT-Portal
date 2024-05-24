# Generated by Django 4.2.9 on 2024-05-24 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datarepo', '0009_fundraised'),
        ('profiles', '0013_alter_researcher_gender_alter_startup_gender_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vc',
            name='area_of_interest',
        ),
        migrations.RemoveField(
            model_name='vc',
            name='funding_stage',
        ),
        migrations.AddField(
            model_name='vc',
            name='area_of_interest',
            field=models.ManyToManyField(blank=True, null=True, to='datarepo.areaofinterest'),
        ),
        migrations.AddField(
            model_name='vc',
            name='funding_stage',
            field=models.ManyToManyField(blank=True, null=True, to='datarepo.preferredinvestmentstage'),
        ),
    ]
