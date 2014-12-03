# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appopinion', '0006_votes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_min', models.DateTimeField()),
                ('date_max', models.DateTimeField()),
                ('title_include', models.CharField(max_length=100, blank=True)),
                ('content_include', models.CharField(max_length=100, blank=True)),
                ('url_include', models.CharField(max_length=100, blank=True)),
                ('min_likecount', models.BigIntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='topic',
            name='likecount',
            field=models.BigIntegerField(default=0),
        ),
    ]
