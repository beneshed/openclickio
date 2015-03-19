# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_lecture_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredlecture',
            name='approved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
