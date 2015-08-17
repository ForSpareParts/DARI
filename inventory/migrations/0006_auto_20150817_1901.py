# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20150817_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='date_received',
            field=models.DateField(null=True, blank=True),
        ),
    ]
