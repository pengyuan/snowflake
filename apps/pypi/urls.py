#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import patterns

urlpatterns = patterns('pypi.views',
    (r'^/?$','pypi'),
    (r'^(\d+)/?$','subject'),
)