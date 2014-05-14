from django.conf.urls import patterns, url
from categories.views import *

urlpatterns = patterns('',
	url(r'^by_group', 'categories.views.by_group'),
	url(r'^by_name', 'categories.views.by_name'),
	url(r'^suggest', 'categories.views.suggest_category'),
	url(r'^(.{1,30})$', 'categories.views.category_detail'),
)