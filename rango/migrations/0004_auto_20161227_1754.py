# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('rango', '0003_page_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='url',
            field=models.URLField(default=''),
        ),
    ]