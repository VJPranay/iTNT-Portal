# Generated by Django 4.2.9 on 2024-03-19 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datarepo', '0005_productdevelopmentstage_revenuestage_and_more'),
        ('registrations', '0009_startupregistrations_company_linkedin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='startupregistrations',
            name='product_development_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.productdevelopmentstage'),
        ),
        migrations.AddField(
            model_name='startupregistrations',
            name='reveune_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.revenuestage'),
        ),
    ]
