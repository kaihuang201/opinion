from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from forms import *
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
        # if user is already signed in
        if request.user.is_authenticated():
            errmsg = 'You are already signed in.'
            form = signupForm()
            return render(request, 'appopinion/signup.html', 
                                {'form':form, 'error':errmsg})

        # handle a sign up request
        uname = request.POST['username']
        pswd = request.POST['password']
        pswdagain = request.POST['password_again']
        
        if pswd!=pswdagain:
            errmsg = 'Passwords does not match.'
            form = signupForm()
            return render(request, 'appopinion/signup.html', 
                                {'form':form, 'error':errmsg})
        else:
            try:
                newuser = User.objects.create_user(uname, password=pswd)
                newuser.save()
            except:
                errmsg = 'Username already existed.'
                form = signupForm()
                return render(request, 'appopinion/signup.html', 
                                {'form':form, 'error':errmsg})
               
            # add the profile 
            profile = Profile(user=newuser, motto = '')
            profile.save()

        # redirect welcome page
        return HttpResponseRedirect(reverse('appopinion:index'))
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
            form = signinForm()
            context = {'form':form, 'authfail':True}
            return render(request, 'appopinion/accountform.html', context)
    else:
        # get requests
        form = signinForm()
        return render(request, 'appopinion/accountform.html', {'form' : form, 'next':next})

"""
signout view, handles signout requests
"""
def signout(request):
    logout(request)
    # redirect signout successful
    return HttpResponseRedirect(reverse('appopinion:index'))


"""
profile edit page
"""
@login_required(login_url='/signin/')
def profile_edit(request):
    usr = request.user
    profile = Profile.objects.get(user=usr)

    if request.method=='POST':
        profile.motto = request.POST['motto']
        profile.save()
        return HttpResponseRedirect(reverse('appopinion:profile'))
        
        """
        passwd = request.POST['password']
        newpass = request.POST['new_pass']
        newpass2 = request.POST['new_pass_again']
        u = authenticate(username=usr.username, password=passwd)
        
        if u is not None:
            if newpass==newpass2 and newpass is not '':
        """
    else:
        context = {
                    'form':profileEditForm(),
                    'user':usr, 
                    'profile':profile,
                  }
        return render(request, 'appopinion/profile_edit.html', context)


"""
profile page
"""
@login_required(login_url='/signin/')
def profile(request):
    usr = request.user
    profile = Profile.objects.get(user=usr)
    context = {
                'user':usr, 
                'profile':profile,
                'liked_topics':profile.likes.all,
              }

    return render(request, 'appopinion/profile.html', context) 

"""
handle like requests
"""
@login_required(login_url='/signin/')
def like(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
    except:
        return HttpResponseRedirect(reverse('appopinion:index'))
    
    usr = request.user
    profile = Profile.objects.get(user=usr)
    
    if not profile.likes.filter(pk=topic_id).exists():
        profile.likes.add(topic)
        profile.save()

        topic.likecount += 1
        topic.save()

    return HttpResponseRedirect(reverse('appopinion:topic_detail', 
                                         args=[topic_id]))

    

"""
signup success page
"""
def success_signup(request):
    return HttpResponse("You have successfully signed up.")


# For index and topic detail
def index(request):
    PAGE_SIZE = 1
    MAX_PAGE_LINK = 3
    MID_PAGES = 1

    topic_all = Topic.objects.all()
    paginator = Paginator(topic_all, PAGE_SIZE)
    page_str = request.GET.get('page')
    try:
        page = int(page_str)
        topic_list = paginator.page(page)
    except PageNotAnInteger:
        topic_list = paginator.page(1)
        page = 1
    except EmptyPage:
        topic_list = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    except:
        page = 1
        topic_list = paginator.page(1)
    
    page_names = []
    
    if (paginator.num_pages > MID_PAGES*2 + 3):

        mid_left = page - MID_PAGES
        if mid_left < 1:
            mid_left = 1

        mid_right = page + MID_PAGES
        if mid_right > paginator.num_pages:
            mid_right = paginator.num_pages

        if mid_left > 1:
            page_names += ['...']

        for i in range(mid_left, mid_right+1):
            page_names += [i]

        if mid_right < paginator.num_pages:
            page_names += ['...']
        """
        if (mid_left <= FIRST_PAGES + 1):
            for i in range(1, page+1):
                page_names += [i]
        else:
            for i in range(1, FIRST_PAGES+1):
                page_names += [i]
            
            page_names += ['...']
            
            for i in range(mid_left, page+1):
                page_names += [i]


        if (mid_right <= paginator.num_pages - LAST_PAGES):
            for i in range(page+1, paginator.num_pages + 1):
                page_names += [i]
        else:
            for i in range(page+1, mid_right+1):
                page_names += [i]
            
            page_names += ['...']
            
            for i in range(paginator.num_pages-LAST_PAGES+1, paginator.num_pages+1):
                page_names += [i]
        """
    else:
        for i in range(1, paginator.num_pages+1):
            page_names += [i]

    page_prev = page - 1
    page_next = page + 1

    if page_next > paginator.num_pages:
        page_next = -1

    context = {
            'topic_list' : topic_list,
            'page_names' : page_names,
            'page_prev' : page_prev,
            'page_next' : page_next,
            'page' : page,
            }

    return render(request, 'appopinion/base.html', context)

def topic_detail(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    
    try:
        comment_text = request.POST['content']
        if comment_text != '':
            if not request.user.is_authenticated():
                return HttpResponseRedirect(
                            reverse('appopinion:signin') +
                            '?next=%s' % request.path)

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

