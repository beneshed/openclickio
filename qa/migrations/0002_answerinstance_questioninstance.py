# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '__first__'),
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('answer_option', models.ForeignKey(to='qa.AnswerOption')),
                ('question', models.ForeignKey(to='qa.Question')),
                ('student', models.ForeignKey(to='accounts.Student')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('question', models.ForeignKey(to='qa.Question')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
