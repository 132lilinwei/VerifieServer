# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-07 13:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20180207_2145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='date published',
        ),
        migrations.AddField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 7, 13, 46, 3, 315522, tzinfo=utc), verbose_name=b'date published'),
        ),
    ]
