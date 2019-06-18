# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('rpwd', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(default=b'Unknown', max_length=10, verbose_name=b'Gender', choices=[(b'Male', b'Male'), (b'Female', b'Female')])),
                ('join_date', models.DateTimeField(auto_now_add=True)),
                ('mobile', models.CharField(max_length=15)),
                ('user_type', models.CharField(default=b'user', max_length=10, verbose_name=b'UserType', choices=[(b'user', b'user'), (b'Admin', b'Admin')])),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
