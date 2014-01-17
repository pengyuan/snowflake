#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Created on 2013-4-27

@author: Eric
'''
from apps.snowflake.models import Category, Description, Node, Topic, Reply, Notice
from django.contrib import admin

admin.site.register(Category)
admin.site.register(Description)
admin.site.register(Node)
admin.site.register(Topic)
admin.site.register(Reply)
admin.site.register(Notice)