# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('short_desc', models.TextField()),
                ('description', models.TextField(null=True, blank=True)),
                ('location', models.CharField(max_length=255, null=True, blank=True)),
                ('contact_details', models.CharField(max_length=255, null=True, blank=True)),
                ('image', models.ImageField(max_length=255, null=True, upload_to=b'%Y/%m/%d', blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('slug', models.SlugField(unique=True, max_length=65)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
