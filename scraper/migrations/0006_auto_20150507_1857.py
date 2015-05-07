# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_averagemarks'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'verbose_name_plural': 'Branches'},
        ),
        migrations.AddField(
            model_name='branch',
            name='codename',
            field=models.CharField(max_length=5, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='section',
            field=models.CharField(max_length=1, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='status',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subject',
            name='max_external',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subject',
            name='max_internal',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(unique=True, max_length=10),
            preserve_default=True,
        ),
    ]
