import json
from django.contrib.auth.decorators import login_required
from dajaxice.decorators import dajaxice_register
from appopinion.models import *


""" handles ajax request like"""
@login_required(login_url='/signin/')
@dajaxice_register
def like(request, topicid):
    if request.is_authenticated():
        print("auth")
    msg = str(topicid)
    return json.dumps({'likecount':likecount})

""" handle ajax for vote """
@dajaxice_register
def vote(request, commentid, up):
    if request.is_authentivated():
        try:
            commentid = int(commentid)
            comment = Comment.objects.get(pk=commentid)
        except:
            # comment not found
            return json.dumps({'change':0})
        
        if up==1:
            change = 1
        else:
            change = -1
        
        comment.vote += change
        comment.save()

        return json.dumps({'commentid':str(commentid), 'change':change})
    else:
        # not signed in
        return json.dumps({'redirect':'/signin/'})
