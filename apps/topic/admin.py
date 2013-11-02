#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Created on 2013-4-27

@author: Eric
'''
from apps.people.models import Notice, Message
from apps.topic.models import Node, Topic, Reply, ParentNode, Description
from django.contrib import admin

admin.site.register(ParentNode)
admin.site.register(Description)
admin.site.register(Node)
admin.site.register(Topic)
admin.site.register(Reply)
admin.site.register(Notice)
admin.site.register(Message)