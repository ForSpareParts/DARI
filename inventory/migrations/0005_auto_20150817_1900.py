# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_auto_20150817_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='date_received',
            field=models.DateField(default=b'', blank=True),
        ),
    ]
