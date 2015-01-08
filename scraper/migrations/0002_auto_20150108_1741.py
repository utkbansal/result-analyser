# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marks',
            old_name='internal',
            new_name='internal_practical',
        ),
        migrations.AddField(
            model_name='marks',
            name='internal_theory',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
