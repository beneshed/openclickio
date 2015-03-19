# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='classes',
            field=models.ManyToManyField(to='core.Lecture'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='university',
            field=models.ForeignKey(to='core.University'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='professor',
            name='lectures',
            field=models.ManyToManyField(related_name='professors_lectures', to='core.Lecture'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='professor',
            name='university',
            field=models.ForeignKey(to='core.University'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='professor',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
