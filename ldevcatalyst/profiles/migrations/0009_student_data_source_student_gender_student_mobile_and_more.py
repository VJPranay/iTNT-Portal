# Generated by Django 4.2.9 on 2024-05-10 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_researcher_data_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='data_source',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='mobile',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='project_guide_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vc',
            name='data_source',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vc',
            name='deal_size_range',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vc',
            name='deal_size_range_usd',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vc',
            name='designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vc',
            name='fund_type',
            field=models.CharField(blank=True, choices=[('angel_investor', 'Angel Investor'), ('angel_network', 'Angel Network'), ('venture_capital', 'Venture Capital Fund'), ('family_office', 'Family Office'), ('corporate_vc', 'Corporate Venture Capital')], default=None, max_length=255, null=True),
        ),
    ]
