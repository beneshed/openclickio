# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import randomslugfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_registeredlecture_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='registration_code',
            field=randomslugfield.fields.RandomSlugField(editable=False, length=7, max_length=7, blank=True, unique=True),
            preserve_default=True,
        ),
    ]
