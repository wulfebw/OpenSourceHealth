from django.conf.urls import patterns, url
from accounts.views import *

urlpatterns = patterns('',
	url(r'^$', 'accounts.views.home'),
	url(r'^settings/$', 'accounts.views.settings'),
    url(r'^logout/$', 'accounts.views.logout'),
)