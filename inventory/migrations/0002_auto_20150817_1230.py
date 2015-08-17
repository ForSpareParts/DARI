# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemrequisition',
            old_name='agent_identifier',
            new_name='checked_out_by',
        ),
    ]
