from django.conf.urls import patterns, url
from projects.views import *

urlpatterns = patterns('',
	url(r'^$', 'projects.views.projects_by_name'),
	url(r'^edit/(?P<project_name>[^/]+)', 'projects.views.edit_project'),
	url(r'^(?P<project_name>[^/]+)/(?P<like>\d{1})', 'projects.views.project_detail'),
	url(r'^(?P<project_name>[^/]+)', 'projects.views.project_detail'),
)