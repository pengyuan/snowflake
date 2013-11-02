#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns('people.views',
    (r'^(\w{3,20})/?$','home'),
)