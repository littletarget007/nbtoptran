# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-06-21 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toptran', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
