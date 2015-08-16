# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=255)),
                ('text', models.TextField(default=b'', blank=True)),
                ('set_on', models.DateTimeField(auto_now_add=True)),
                ('alert_on', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('cleared_on', models.DateTimeField(null=True, blank=True)),
            ],
        ),
    ]
