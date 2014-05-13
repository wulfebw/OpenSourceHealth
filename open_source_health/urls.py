from django.conf.urls import patterns, include, url
from django.shortcuts import redirect

from categories import views


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^categories/', include('categories.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^$', 'categories.views.by_group'),
    url('', include('social.apps.django_app.urls', namespace='social')),

    # hack on python social to ignore "next" parameters. I'm not sure how it handles it internally, so this will work for now.
    url(r'^accounts/login/', lambda x: redirect('/login/github/')),
)
