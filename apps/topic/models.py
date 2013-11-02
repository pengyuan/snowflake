#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.topic import widgets
from django.contrib.admin import widgets as admin_widgets
from django.contrib.auth.models import User
from django.db import models

class MarkDownField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {'widget': widgets.MarkDownInput}
        defaults.update(kwargs)
        
        if defaults['widget'] == admin_widgets.AdminTextareaWidget:
            defaults['widget'] = widgets.AdminMarkDownInput
        
        return super(MarkDownField, self).formfield(**defaults)

#节点：节点名称，节点英文slug，节点描述，创建时间，最后更新时间，话题数目
class ParentNode(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
       
#节点：节点名称，节点英文slug，创建时间，最后更新时间，话题数目，父节点
class Node(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    num_topics = models.IntegerField(default=0)
    category = models.ForeignKey(ParentNode)

    def __unicode__(self):
        return self.name
    
#节点描述：内容，作者，节点，时间，是否正在使用
class Description(models.Model):
    content = MarkDownField()
    author = models.ForeignKey(User)
    node = models.ForeignKey(Node)
    time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
     
    def __unicode__(self):
        return self.content
    
#话题：标题，内容，所属节点，作者，查看次数，回复次数，创建时间，最后更新时间
class Topic(models.Model):
    title = models.CharField(max_length=100)
    #content = models.TextField()  
    content = MarkDownField()
    #content_html = MarkDownField(editable=False,blank=True)
    node = models.ForeignKey(Node)
    author = models.ForeignKey(User,related_name='+')
    num_views = models.IntegerField(default=0)
    num_replies = models.PositiveSmallIntegerField(default=0)
    last_reply = models.ForeignKey(User,related_name='+',null=True)
    created_on = models.DateTimeField(auto_now_add=True)      #第一次创建时加入当前时间
    updated_on = models.DateTimeField(blank=True, null=True)   #最后一次回复
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/topic/%i/" % self.id

#回复：内容，所属话题，作者，创建时间
class Reply(models.Model):
    #content = models.TextField()
    content = MarkDownField()
    #content_html = MarkDownField(editable=False,blank=True)
    author = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)
    has_parent = models.BooleanField(default=False)
    parent = models.ForeignKey('self',null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content