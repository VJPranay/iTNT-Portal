# Generated by Django 4.2.9 on 2024-02-28 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datarepo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.district'),
        ),
    ]