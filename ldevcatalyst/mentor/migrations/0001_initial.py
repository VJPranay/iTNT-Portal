# Generated by Django 4.2.9 on 2024-06-20 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('datarepo', '0009_fundraised'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('prefer not to say', 'Prefer not to say')], max_length=100, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='mentor_profile_pictures')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('designation', models.CharField(blank=True, max_length=255, null=True)),
                ('linkedin_url', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_bio', models.FileField(blank=True, null=True, upload_to='mentor_bios')),
                ('certified_mentor', models.BooleanField(blank=True, null=True)),
                ('functional_areas_of_expertise', models.CharField(blank=True, max_length=255, null=True)),
                ('mentoring_experience', models.CharField(blank=True, max_length=255, null=True)),
                ('motivation_for_mentoring', models.CharField(blank=True, max_length=255, null=True)),
                ('category_represent_you', models.CharField(blank=True, max_length=255, null=True)),
                ('mentees_journey', models.CharField(blank=True, max_length=255, null=True)),
                ('area_of_intrest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.areaofinterest')),
            ],
        ),
    ]
