# Generated by Django 4.2.9 on 2024-03-25 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0019_alter_industryregistrations_mobile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vcregistrations',
            name='deal_size_range_usd',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]