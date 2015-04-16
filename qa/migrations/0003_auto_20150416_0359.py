# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '__first__'),
        ('qa', '0002_answerinstance_questioninstance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questioninstance',
            name='question',
        ),
        migrations.DeleteModel(
            name='QuestionInstance',
        ),
        migrations.AddField(
            model_name='question',
            name='lecture',
            field=models.ForeignKey(related_name='belongs_to', blank=True, to='core.Lecture', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
