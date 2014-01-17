#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# automatic admin interface
admin.autodiscover()

# snowflake app's url settings
urlpatterns = patterns('apps.snowflake.views',
    (r'^$','index'),
    (r'^recent/?$','recent'),
    (r'^hot/?$','hot'),
    (r'^node/(\w+)/?$','node'),
    (r'^node/(\w+)/new/?$','new'),
    (r'^node/(\w+)/edit/?$','edit'),
    (r'^node/(\w+)/choose/?$','choose'),  
    (r'^topic/(\d+)/?$','topic'),
    (r'^topic/(\d+)/reply/?$','reply'),
    (r'^user/(\w{3,20})/?$','home'),
    (r'^notice/?$','notice'),
    (r'^notice/(\d+)/delete/?$','delete'),
    (r'^ajax_thank/?$','ajax_thank'),
)

# accounts app's url settings
urlpatterns += patterns('',
    (r'^accounts/',include('apps.accounts.urls')),
)

# automatic admin interface's url settings
urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)

# serve static files in development environment
urlpatterns += staticfiles_urlpatterns()


# add your own self-defined page's url at here
urlpatterns += patterns('apps.snowflake.views',
    (r'^about/?$','about'),
)