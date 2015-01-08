# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20150108_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='marks',
            name='credits',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
