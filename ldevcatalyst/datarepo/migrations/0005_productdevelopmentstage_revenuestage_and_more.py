# Generated by Django 4.2.9 on 2024-03-19 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datarepo', '0004_areaofinterest_is_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDevelopmentStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('serial', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RevenueStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('serial', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='preferredinvestmentstage',
            name='serial',
            field=models.IntegerField(default=0),
        ),
    ]
