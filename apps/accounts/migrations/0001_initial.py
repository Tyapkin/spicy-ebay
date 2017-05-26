# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 12:12
from __future__ import unicode_literals

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
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runame', models.CharField(max_length=254, unique=True, verbose_name='ruName')),
                ('app_id', models.CharField(max_length=254, unique=True, verbose_name='app id')),
                ('dev_id', models.CharField(blank=True, default='', max_length=254, verbose_name='dev id')),
                ('cert_id', models.CharField(blank=True, default='', max_length=254, verbose_name='cert id')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
        ),
    ]
