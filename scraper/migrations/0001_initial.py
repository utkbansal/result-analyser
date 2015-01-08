# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('theory', models.IntegerField()),
                ('practical', models.IntegerField()),
                ('internal', models.IntegerField()),
                ('semester', models.IntegerField()),
                ('back', models.BooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('roll_no', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('fathers_name', models.CharField(max_length=255)),
                ('branch', models.ForeignKey(to='scraper.Branch')),
                ('college', models.ForeignKey(to='scraper.College')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='marks',
            name='student',
            field=models.ForeignKey(to='scraper.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='marks',
            name='subject',
            field=models.ForeignKey(to='scraper.Subject'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='marks',
            unique_together=set([('subject', 'student')]),
        ),
    ]
