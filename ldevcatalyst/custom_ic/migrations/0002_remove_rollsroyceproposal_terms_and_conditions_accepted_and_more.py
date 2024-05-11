# Generated by Django 4.2.9 on 2024-05-11 04:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('custom_ic', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rollsroyceproposal',
            name='terms_and_conditions_accepted',
        ),
        migrations.AddField(
            model_name='rollsroyceproposal',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rollsroyceproposal',
            name='status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='rollsroyceproposal',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]