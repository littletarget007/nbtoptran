# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-06-23 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toptran', '0014_auto_20180623_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
