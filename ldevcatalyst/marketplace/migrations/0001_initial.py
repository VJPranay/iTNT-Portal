# Generated by Django 4.2.9 on 2024-02-01 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0005_startup_short_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('breif', models.TextField(blank=True, null=True)),
                ('value_proposition', models.TextField(blank=True, null=True)),
                ('solution_advantage', models.TextField(blank=True, null=True)),
                ('service_readiness', models.TextField(blank=True, null=True)),
                ('implementation_time', models.TextField(blank=True, null=True)),
                ('ip_status', models.CharField(blank=True, choices=[('not_applicable', 'not_applicable'), ('granted', 'granted'), ('published', 'published'), ('expired', 'expired')], max_length=100, null=True)),
                ('start_up', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.startup')),
            ],
        ),
        migrations.CreateModel(
            name='TangibleBenfits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketplace.services')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('breif', models.TextField(blank=True, null=True)),
                ('value_proposition', models.TextField(blank=True, null=True)),
                ('solution_advantage', models.TextField(blank=True, null=True)),
                ('product_readiness', models.TextField(blank=True, null=True)),
                ('implementation_time', models.TextField(blank=True, null=True)),
                ('ip_status', models.CharField(blank=True, choices=[('not_applicable', 'not_applicable'), ('granted', 'granted'), ('published', 'published'), ('expired', 'expired')], max_length=100, null=True)),
                ('start_up', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.startup')),
            ],
        ),
        migrations.CreateModel(
            name='ProductBenfits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='marketplace.products')),
            ],
        ),
    ]