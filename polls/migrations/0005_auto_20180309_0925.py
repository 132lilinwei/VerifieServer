# Generated by Django 2.0.2 on 2018-03-09 01:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20180207_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 9, 1, 25, 53, 332225, tzinfo=utc), verbose_name='date published'),
        ),
    ]
