import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import pickle

import os,sys
import django

def word_feats(words):
    return dict([(word, True) for word in words])

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE']='opinion.settings'

print "Reading Classifier"
f = open('SentimentClassifier.pickle')
sentimentClassifier = pickle.load(f)
f.close()

from django.contrib.auth.models import User
from appopinion.models import *

users = User.objects.all()
django.setup()

comments = Comment.objects.all()
for comment in comments:
    print comment.content
    comment.positive = sentimentClassifier.classify(word_feats(comment.content)) == "pos"
    print comment.positive
    comment.save()