# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appopinion', '0006_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='positive',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='likecount',
            field=models.BigIntegerField(default=0),
            preserve_default=True,
        ),
    ]
