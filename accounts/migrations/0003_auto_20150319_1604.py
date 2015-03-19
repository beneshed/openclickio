# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150319_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='lectures',
            field=models.ManyToManyField(related_name='professors_lectures', null=True, to='core.Lecture', blank=True),
            preserve_default=True,
        ),
    ]
