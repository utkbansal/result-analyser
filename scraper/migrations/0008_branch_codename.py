# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0007_student_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='codename',
            field=models.CharField(max_length=5, blank=True),
            preserve_default=True,
        ),
    ]
