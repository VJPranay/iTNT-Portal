# Generated by Django 4.2.9 on 2024-03-25 04:49

from django.db import migrations, models
import registrations.models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0016_startupregistrations_fund_raised_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='vcregistrations',
            name='company_portfolio_document',
            field=models.FileField(blank=True, null=True, upload_to='portfolio_documents/', validators=[registrations.models.validate_file_size]),
        ),
        migrations.AddField(
            model_name='vcregistrations',
            name='deal_size_range',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vcregistrations',
            name='designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
