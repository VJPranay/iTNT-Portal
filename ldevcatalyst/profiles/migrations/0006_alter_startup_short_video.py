# Generated by Django 4.2.9 on 2024-02-16 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_startup_short_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='short_video',
            field=models.URLField(blank=True, null=True),
        ),
    ]