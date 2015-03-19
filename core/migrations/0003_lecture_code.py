# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150319_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='code',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
