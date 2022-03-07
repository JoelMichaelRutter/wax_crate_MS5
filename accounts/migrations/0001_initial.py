# Generated by Django 3.2 on 2022-03-07 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('account_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('account_postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('account_town_or_city', models.CharField(blank=True, max_length=40, null=True)),
                ('account_street_address1', models.CharField(blank=True, max_length=80, null=True)),
                ('account_street_address2', models.CharField(blank=True, max_length=80, null=True)),
                ('account_county', models.CharField(blank=True, max_length=80, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
