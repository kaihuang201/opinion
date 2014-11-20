import json
from dajaxice.decorators import dajaxice_register
from appopinion.models import *


""" handles ajax request like"""
@dajaxice_register
def like(request, topicid):
    msg = str(topicid)
    return json.dumps({'likecount':likecount})

""" handle ajax for vote """
@dajaxice_register
def vote(request, commentid, up):
    if request.user.is_authenticated():
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
        print("")
        return json.dumps({'redirect':'/signin/'})
