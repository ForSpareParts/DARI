# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('material_number', models.CharField(max_length=255)),
                ('serial_number', models.CharField(default=b'', max_length=255, blank=True)),
                ('date_received', models.DateField()),
                ('kit', models.CharField(default=b'', max_length=255, blank=True)),
                ('notes', models.TextField(default=b'', blank=True)),
                ('sort_by_name', models.CharField(max_length=255)),
                ('manual', models.TextField(default=b'', blank=True)),
                ('qty_at_inventory', models.PositiveIntegerField(default=1, blank=True)),
                ('inventory_loaded_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified_on', models.DateTimeField(auto_now=True)),
                ('current_qty', models.IntegerField(blank=True)),
                ('superceded_by', models.ForeignKey(blank=True, to='inventory.Item', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemRequisition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('checked_out_on', models.DateTimeField(auto_now_add=True)),
                ('checked_in_on', models.DateTimeField()),
                ('agent_identifier', models.CharField(max_length=255)),
                ('last_modified_on', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(to='inventory.Item')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('category', 'name', 'serial_number', 'superceded_by')]),
        ),
    ]