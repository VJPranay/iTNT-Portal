# Generated by Django 5.0.2 on 2024-02-17 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0018_vcregistrations_deal_size_range_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentregistrations',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
