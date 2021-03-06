# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 21:46
from __future__ import unicode_literals

from django.db import migrations

from common.db.operations import json_gin_index
from core.models import Entry, Event, Ledger

operations = json_gin_index(Ledger, 'metadata')
operations += json_gin_index(Event, 'metadata')
operations += json_gin_index(Entry, 'metadata')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_temporal_table'),
    ]

    operations = operations
