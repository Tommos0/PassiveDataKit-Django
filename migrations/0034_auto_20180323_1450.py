# pylint: skip-file

# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-23 14:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('passive_data_kit', '0033_datapoint_user_agent'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='datapoint',
            index_together=set([('source', 'generator_identifier', 'secondary_identifier'), ('generator_identifier', 'recorded'), ('source', 'generator_identifier'), ('generator_identifier', 'secondary_identifier', 'recorded'), ('source', 'created'), ('generator_identifier', 'secondary_identifier'), ('source', 'generator_identifier', 'secondary_identifier', 'recorded'), ('source', 'generator_identifier', 'secondary_identifier', 'created'), ('generator_identifier', 'created', 'recorded'), ('source', 'generator_identifier', 'created'), ('generator_identifier', 'secondary_identifier', 'created'), ('source', 'generator_identifier', 'created', 'recorded'), ('generator_identifier', 'created'), ('generator_identifier', 'secondary_identifier', 'created', 'recorded'), ('source', 'generator_identifier', 'secondary_identifier', 'created', 'recorded'), ('source', 'user_agent'), ('source', 'generator_identifier', 'recorded')]),
        ),
    ]
