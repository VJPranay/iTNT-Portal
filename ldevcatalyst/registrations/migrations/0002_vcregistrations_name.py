# Generated by Django 4.2.9 on 2024-05-14 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vcregistrations',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]