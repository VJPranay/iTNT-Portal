# Generated by Django 4.2.9 on 2024-02-01 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datarepo', '0002_industrycategory'),
        ('profiles', '0002_alter_user_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('inventors', models.CharField(blank=True, max_length=255, null=True)),
                ('filing_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('paper_link', models.URLField(blank=True, null=True)),
                ('journal', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_name', models.CharField(blank=True, max_length=100, null=True)),
                ('firm_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('company_website', models.URLField(blank=True, null=True)),
                ('linkedin_profile', models.URLField(blank=True, null=True)),
                ('area_of_interest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.areaofinterest')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.district')),
                ('funding_stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.preferredinvestmentstage')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.state')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('year_of_graduation', models.PositiveIntegerField(blank=True, null=True)),
                ('project_idea', models.TextField(blank=True, null=True)),
                ('area_of_interest', models.ManyToManyField(to='datarepo.areaofinterest')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.department')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.district')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.institution')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.state')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StartUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('co_founder_count', models.PositiveIntegerField(blank=True, null=True)),
                ('founder_names', models.CharField(blank=True, max_length=255, null=True)),
                ('team_size', models.PositiveIntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('dpiit_number', models.CharField(blank=True, max_length=20, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('pitch_deck', models.FileField(blank=True, null=True, upload_to='pitch_decks/')),
                ('video_link', models.URLField(blank=True, null=True)),
                ('area_of_interest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.areaofinterest')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.district')),
                ('funding_stage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.preferredinvestmentstage')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.state')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='researcher_pictures/')),
                ('highest_qualification', models.CharField(blank=True, max_length=100, null=True)),
                ('area_of_interest', models.ManyToManyField(to='datarepo.areaofinterest')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.department')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.district')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.institution')),
                ('patents', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.patent')),
                ('publications', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.publication')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.state')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('point_of_contact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('area_of_interest', models.ManyToManyField(to='datarepo.areaofinterest')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.district')),
                ('industry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.industrycategory')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datarepo.state')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
