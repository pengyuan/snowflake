#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import patterns
urlpatterns = patterns("django.contrib.auth.views",
    (r'^password_change/?$', 'password_change'), 
    (r'^password_change/done/?$', 'password_change_done'), 
    (r'^password_reset/?$', 'password_reset',{
        'template_name': 'registration/password_reset_form.html',
        'email_template_name':'registration/password_reset_email.html',
        'subject_template_name': 'registration/password_reset_subject.txt',
        'from_email': '"Pythonic社区" <no-reply@pythonic.org>'
    }), 
    (r'^password_reset/done/?$', 'password_reset_done'), 
    (r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/?$', 'password_reset_confirm'), 
    (r'^reset/done/?$', 'password_reset_complete'),
)            
           
urlpatterns += patterns('accounts.views',
    (r'^settings/?$','settings'),
    (r'^login/?$','login'),
    (r'^logout/?$','logout'),                
    (r'^register/?$','register'),
    (r'^active/(\w{1,10})/(.*)/?$','active'),
)