# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-06-21 16:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toptran', '0003_auto_20180621_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='image',
        ),
    ]
