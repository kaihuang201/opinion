# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appopinion', '0002_auto_20141114_0431'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='likes',
            field=models.ManyToManyField(to='appopinion.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topic',
            name='likecount',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
