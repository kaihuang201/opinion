from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils import timezone

from forms import *
from appopinion.models import *

from datetime import datetime
from dateutil.tz import tzlocal
from django.db import connection
import re
import cgi
import json

"""Feature function for comments"""
def word_feats(words):
    return dict([(word, True) for word in words])

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

"""
helper funtion for getting context for index page, takes a queryset topics and page_str, return the context
"""
def getTopicListContext(topics, page_str):
    PAGE_SIZE = 30
    MAX_PAGE_LINK = 10
    MID_PAGES = 3
    
    paginator = Paginator(topics, PAGE_SIZE)
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
    return context 

# For index and topic detail
def index(request):
    page_str = '1'
    search_str = request.GET.get('search')

    if search_str is not None:
        topics = Topic.objects.filter(
                                            Q(title__contains=search_str) | 
                                            Q(content__contains=search_str) |
                                            Q(url__contains=search_str) |
                                            Q(source__contains=search_str)
                                        )
    else:
        topics = Topic.objects.all()
        page_str = request.GET.get('page')

    context = getTopicListContext(topics, page_str)
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
                                  positive = True,
                                  )
            new_comment.save()
    except:
        pass
    
    comment_list = Comment.objects.all().filter(parent_id=topic_id)

    pos_count = 0.0
    for comment in comment_list:
        if comment.positive == True:
            pos_count += 1.0
    if len(comment_list ) > 0:
        pos_percent = pos_count / len(comment_list)
        neg_percent = 1.0 - pos_percent
    else:
        pos_percent = 0.0
        neg_percent = 0.0
    print pos_percent
    return render(request, 'appopinion/topic_detail.html', {'topic_id':topic_id, 'topic':topic, 'comment_list':comment_list[::-1], 'pos_percent': pos_percent * 100, 'neg_percent': neg_percent * 100})


"""
handle advance search request
"""
def search(request):
    if request.method=='POST':
        try:
            after_str = request.POST.get('after')
            after = datetime.strptime('1970/01/01', '%Y/%m/%d')
            if not after_str=='':
                after = datetime.strptime(after_str, '%Y/%m/%d')

            before_str = request.POST.get('before')
            before = datetime.now()
            if not before_str=='':
                before = datetime.strptime(before_str, '%Y/%m/%d')

            title_include = request.POST.get('title_include')
            if title_include == '':
                title_include = ' '

            min_like_str = request.POST.get('min_like')
            min_like = -1
            if not min_like_str=='':
                min_like = int(min_like_str)

            topics = Topic.objects.filter(date__gt=after, date__lt=before, likecount__gt=min_like, title__contains=title_include)

            return render(request, 'appopinion/base.html', {'topic_list':topics})
        except:
            form = searchForm()
            return render(request, 'appopinion/search.html', {'error':'There is an error in your query, please try again.',
                                                            'form':form})
    else:
        form = searchForm()
        return render(request, 'appopinion/search.html', {'form':form})


@csrf_exempt
def topic_update(request, topic_id):
    response_data = {}
    if request.user.is_authenticated():
        response_data['auth'] = 1
    else:
        response_data['auth'] = 0
    ensure_csrf_cookie(request)

    time = request.POST['now']
    try:
        time = datetime.fromtimestamp(int(time)/1e3)
        comment_list = Comment.objects.all().filter(parent_id=topic_id, date__gt=time)
        
        counter = 0
        
        for comment in comment_list:
            response_data[str(counter)] = {'content': comment.content, 'commentid': comment.id, 'vote':comment.vote}
            counter += 1
        print response_data
    except Exception as e:
        print e
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")

