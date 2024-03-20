# Generated by Django 4.2.9 on 2024-03-20 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datarepo', '0005_productdevelopmentstage_revenuestage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areaofinterest',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='industrycategory',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='preferredinvestmentstage',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='productdevelopmentstage',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='revenuestage',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
