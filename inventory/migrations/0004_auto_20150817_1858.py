# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20150817_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='material_number',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
