# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0008_branch_codename'),
    ]

    operations = [
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
    ]
