# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150319_1323'),
        ('qa', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='questions',
            field=models.ManyToManyField(to='qa.Question', through='qa.LectureQuestion', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lecture',
            name='roster',
            field=models.ManyToManyField(to='accounts.Student', through='core.RegisteredLecture', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lecture',
            name='university',
            field=models.ForeignKey(to='core.University'),
            preserve_default=True,
        ),
    ]
