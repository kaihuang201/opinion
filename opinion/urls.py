from django.conf.urls import patterns, include, url
from django.contrib import admin

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('appopinion.urls', namespace='appopinion')),
)
