from django.conf.urls import patterns, include, url
from appopinion import views

urlpatterns = patterns('',
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit'),
    
    url(r'^topic_id=(?P<topic_id>[0-9]+)/$', views.topic_detail, name='topic_detail'),
    url(r'^$', views.index, name='index'),

    url(r'^(?P<topic_id>[0-9]+)/like/$', views.like, name='like'),
)
