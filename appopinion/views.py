from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from forms import signinForm, signupForm
from appopinion.models import *

from datetime import datetime
from django.db import connection
import re
import cgi



"""
signup view, handles signup requests.
"""
def signup(request):
    if request.method=='POST':
        uname = request.POST['username']
        pswd = request.POST['password']
        pswdagain = request.POST['password_again']
        
        if pswd==pswdagain:
            try:
                newuser = User.objects.create_user(uname, password=pswd)
                newuser.save()
            except:
                errmsg = 'Username already existed!'
                form = signupForm()
                return render(request, 'appopinion/signup.html', {'form':form, 'errmsg':errmsg})
               
            # add the profile 
            profile = Profile(user=newuser, motto = '')
            profile.save()

        # redirect welcome page
        return HttpResponseRedirect(reverse('appopinion:success_signup'))
    else:

        # get request
        form = signupForm()
        return render(request, 'appopinion/signup.html', {'form' : form})
        
"""
signin view, handles signin requests.
"""
def signin(request):
    if request.method=='POST':
        uname = request.POST['username']
        passwd = request.POST['password']
        
        user = authenticate(username=uname, password=passwd)
        
        if user is not None and user.is_active:
            # auth successful Redirect to a success page.
            login(request, user)
            return HttpResponseRedirect(reverse('appopinion:index'))
        else:
            #auth failure
            return HttpResponse("auth failure")
    else:
        # get requests
        form = signinForm()
        return render(request, 'appopinion/accountform.html', {'form' : form})

"""
signout view, handles signout requests
"""
def signout(request):
    logout(request)
    # redirect signout successful
    return HttpResponseRedirect(reverse('appopinion:success_signout'))

"""
profile page
"""
def profile(request):
    usr = request.user
    profile = Profile.objects.get(user=usr)
    
    return render(request, 'appopinion/profile.html', {'user':usr, 
                                                       'profile':profile,
                                                       'liked_topics':profile.likes.all,
                                                   })

"""
signout success page
"""
def success_signout(request):
    return HttpResponse("You have successfully signed out.")

"""
signup success page
"""
def success_signup(request):
    return HttpResponse("You have successfully signed up.")


# For index and topic detail
def index(request):
    topic_list = Topic.objects.all()
    return render(request, 'appopinion/base.html', {'topic_list' : topic_list[:36]})

def topic_detail(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    
    try:
        comment_text = request.POST['content']
        new_comment = Comment(
                              parent_id = topic_id,
                              content = cgi.escape(comment_text, True),
                              date = datetime.now(),
                              )
        new_comment.save()
    except:
        pass
    
    comment_list = Comment.objects.all().filter(parent_id=topic_id)
    return render(request, 'appopinion/topic_detail.html', {'topic_id':topic_id, 'topic':topic, 'comment_list':comment_list})

