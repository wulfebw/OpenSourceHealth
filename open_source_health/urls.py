from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^categories/', include('categories.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url('', include('social.apps.django_app.urls', namespace='social'))
)
