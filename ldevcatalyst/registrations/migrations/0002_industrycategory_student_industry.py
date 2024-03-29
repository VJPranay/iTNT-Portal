# Generated by Django 4.2.9 on 2024-01-31 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndustryCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('year_of_graduation', models.PositiveIntegerField()),
                ('project_idea', models.TextField()),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registrations.department')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registrations.district')),
                ('domain_of_interest', models.ManyToManyField(to='registrations.areaofinterest')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registrations.institution')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registrations.state')),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('point_of_contact_name', models.CharField(max_length=100)),
                ('poc_mail_id', models.EmailField(max_length=254)),
                ('poc_contact_number', models.CharField(max_length=15)),
                ('area_of_interest_for_collaboration', models.ManyToManyField(to='registrations.areaofinterest')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registrations.district')),
                ('industry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registrations.industrycategory')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registrations.state')),
            ],
        ),
    ]
