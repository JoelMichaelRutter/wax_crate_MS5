# Generated by Django 3.2 on 2022-03-15 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_auto_20220311_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='genre',
            field=models.CharField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='condition',
            field=models.CharField(choices=[('M', 'mint'), ('NM', 'near_mint'), ('VG', 'very_good'), ('G', 'good'), ('F', 'fair'), ('P', 'poor')], default='mint', max_length=9),
        ),
    ]