# pylint: skip-file

# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-02 17:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passive_data_kit', '0039_dataservermetadatum_last_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataservermetadatum',
            options={'verbose_name_plural': 'data server metadata'},
        ),
    ]
