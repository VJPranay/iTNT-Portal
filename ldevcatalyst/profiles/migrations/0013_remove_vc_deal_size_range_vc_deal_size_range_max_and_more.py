# Generated by Django 4.0.5 on 2024-02-20 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_vc_deal_size_range_vc_portfolio_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vc',
            name='deal_size_range',
        ),
        migrations.AddField(
            model_name='vc',
            name='deal_size_range_max',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vc',
            name='deal_size_range_min',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
