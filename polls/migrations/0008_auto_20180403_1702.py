# Generated by Django 2.0.3 on 2018-04-03 09:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20180311_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 3, 9, 2, 13, 58424, tzinfo=utc), verbose_name='date published'),
        ),
    ]