# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_marks_credits'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marks',
            old_name='credits',
            new_name='credit',
        ),
    ]
