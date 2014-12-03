from django.db import models
from django.contrib.auth.models import User

"""Topic Model"""
class Topic(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField('date published')
    content = models.TextField()
    url = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    likecount = models.BigIntegerField(default=0)

"""Comment Model"""
class Comment(models.Model):
    content = models.TextField()
    parent = models.ForeignKey(Topic)
    date = models.DateTimeField('date published')
    vote = models.BigIntegerField(default=0)
    positive = models.BooleanField(default=True)

"""Profile Model"""
class Profile(models.Model):
    user = models.ForeignKey(User)
    motto = models.CharField(max_length=200, blank=True)
    likes = models.ManyToManyField(Topic, blank=True)

"""Store what each user voted what"""
class Votes(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
    voteval = models.IntegerField(default=0)
