#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.db import models
from django.db.models.signals import post_save
import settings

# category model
class Category(models.Model):
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
       
# node model
class Node(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    num_topics = models.IntegerField(default=0)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name
    
# node description model
class Description(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    node = models.ForeignKey(Node)
    time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
     
    def __unicode__(self):
        return self.content
    
# topic model
class Topic(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()  
    node = models.ForeignKey(Node)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='+')
    num_views = models.IntegerField(default=0)
    num_replies = models.IntegerField(default=0)
    last_reply = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='+')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return self.title


# reply model
class Reply(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='+')
    topic = models.ForeignKey(Topic)
    created_on = models.DateTimeField(auto_now_add=True)
    thank_set = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='+')

    def __unicode__(self):
        return self.content
    

# notice model
class Notice(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='+')   #not to create a backwards relation
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='+')
    topic = models.ForeignKey(Topic,null=True)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_readed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content
    
def create_notice(sender, **kwargs):
    reply = kwargs['instance']   
    if reply.author != reply.topic.author:      # don't create notice when you reply to yourself
        Notice.objects.create(from_user=reply.author,to_user=reply.topic.author,topic=reply.topic,content=reply.content)
    
post_save.connect(create_notice, sender=Reply)