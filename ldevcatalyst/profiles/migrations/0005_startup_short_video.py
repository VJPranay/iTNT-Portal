# Generated by Django 4.2.9 on 2024-02-01 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_industry_created_industry_updated_patent_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='short_video',
            field=models.FileField(blank=True, null=True, upload_to='short_video/'),
        ),
    ]
