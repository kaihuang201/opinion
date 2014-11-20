# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appopinion', '0004_auto_20141114_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='vote',
            field=models.BigIntegerField(default=0),
            preserve_default=True,
        ),
    ]
