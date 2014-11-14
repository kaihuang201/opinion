# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appopinion', '0003_auto_20141114_0519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='likes',
            field=models.ManyToManyField(to=b'appopinion.Topic', blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='motto',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
