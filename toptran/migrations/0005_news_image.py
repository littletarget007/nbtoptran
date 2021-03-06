# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-06-22 01:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('toptran', '0004_remove_news_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news_image', to=settings.FILER_IMAGE_MODEL),
        ),
    ]
