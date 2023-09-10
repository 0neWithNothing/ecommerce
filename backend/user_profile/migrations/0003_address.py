# Generated by Django 4.2.5 on 2023-09-10 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_user_groups_user_user_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=80)),
                ('region', models.CharField(blank=True, max_length=80)),
                ('city', models.CharField(blank=True, max_length=80)),
                ('address', models.CharField(blank=True, max_length=40)),
                ('zip_code', models.CharField(blank=True, max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
