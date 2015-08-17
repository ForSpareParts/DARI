# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20150817_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='shipment',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('category', 'name', 'material_number', 'serial_number', 'superceded_by')]),
        ),
    ]
