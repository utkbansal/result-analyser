# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_colleges(apps, schema_editor):
    College = apps.get_model('scraper', 'College')
    c= College(name='AKGEC', code='027')
    c.save()
    c = College(name='KIET', code='029')
    c.save()
    c = College(name='JSS', code='091')
    c.save()
    c = College(name='ABES', code='032')
    c.save()


def add_branches(apps, schema_editor):
    Branch = apps.get_model('scraper', 'Branch')

    b = Branch(name='Computer Science and Engineering',
               code='10',
               codename='CSE')
    b.save()

    b = Branch(name='Information Technology',
               code='13',
               codename='IT')
    b.save()

    b = Branch(name='Electrical & Electronics Engineering',
               code='21',
               codename='EN')
    b.save()

    b = Branch(name='Electronics and Communication Engineering',
               code='31',
               codename='ECE')
    b.save()

    b = Branch(name='Electronics and Instrumentation Engineering',
               code='32',
               codename='EI')
    b.save()

    b = Branch(name='Civil Engineering',
               code='00',
               codename='CE')
    b.save()

    b = Branch(name='Mechanical Engineering',
               code='40',
               codename='ME')
    b.save()

class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0006_auto_20150507_1857'),
    ]

    operations = [
        migrations.RunPython(add_colleges),
        migrations.RunPython(add_branches),
    ]