# Generated by Django 3.2 on 2022-03-08 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customeraccount_favoured_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customeraccount',
            name='account_email',
        ),
        migrations.RemoveField(
            model_name='customeraccount',
            name='account_full_name',
        ),
        migrations.RemoveField(
            model_name='customeraccount',
            name='favoured_genre',
        ),
    ]
