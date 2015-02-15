# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_auto_20150114_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='AverageMarks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('semester', models.IntegerField()),
                ('average', models.IntegerField()),
                ('maximum', models.IntegerField()),
                ('minimum', models.IntegerField()),
                ('branch', models.ForeignKey(to='scraper.Branch')),
                ('college', models.ForeignKey(to='scraper.College')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
