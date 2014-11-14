from django.db import models
from django.contrib.auth.models import User

"""Profile Model"""
class Profile(models.Model):
    user = models.ForeignKey(User)
    motto = models.CharField(max_length=200)

"""Topic Model"""
class Topic(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField('date published')
    content = models.TextField()
    url = models.CharField(max_length=255)
    source = models.CharField(max_length=255)

"""Comment Model"""
class Comment(models.Model):
    content = models.TextField()
    parent = models.ForeignKey(Topic)
    date = models.DateTimeField('date published')