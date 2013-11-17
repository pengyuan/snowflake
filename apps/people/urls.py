#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns('people.views',
    (r'^(\w{3,20})/?$','home'),
    (r'^(\w{3,20})/reply/?$','reply'),
    (r'^(\w{3,20})/thank/?$','thank'),
    (r'^(\w{3,20})/like/?$','like'),
)