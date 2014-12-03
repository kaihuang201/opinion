# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appopinion', '0007_auto_20141203_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='search',
            name='user',
        ),
        migrations.DeleteModel(
            name='Search',
        ),
    ]
