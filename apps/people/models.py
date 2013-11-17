#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.topic.models import Topic, Reply
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
       #html = [u'<div class="wmd-panel resizable-textarea"><div id="wmd-button-bar"></div><span><textarea class="span12 resizable processed" cols="40" id="id_content" name="content" rows="10"></textarea><div class="grippie" style="margin-right: 0px;"></div></span>']

class Notice(models.Model):
    sender = models.ForeignKey(User,related_name='+') #not to create a backwards relation
    recipient = models.ForeignKey(User,related_name='+')
    is_topic = models.BooleanField()
    topic = models.ForeignKey(Topic,null=True)
    reply = models.ForeignKey(Reply,null=True)
    content = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    is_readed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content
    
class Message(models.Model):
    is_sender = models.BooleanField()
    talk_to = models.ForeignKey(User,related_name='+')
    belong_to = models.ForeignKey(User,related_name='+')
    content = models.CharField(max_length=200,blank=False)
    time = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    is_readed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content
    
def create_notice(sender, **kwargs):
    reply = kwargs['instance']   
    if reply.has_parent:
        if reply.author != reply.parent.author:     #可以回复自己的回复，但是不新建提醒
            Notice.objects.create(sender=reply.author,recipient=reply.parent.author,is_topic=False,topic=reply.topic,reply=reply.parent,content=reply.content)
    else:
        if reply.author != reply.topic.author:      #可以回复自己的话题，但是不新建提醒
            Notice.objects.create(sender=reply.author,recipient=reply.topic.author,is_topic=True,topic=reply.topic,content=reply.content)
    
post_save.connect(create_notice, sender=Reply)


#我关注的用户
# class Follow(models.Model):
#     user = models.ForeignKey(User,related_name='+')
#     follow = models.ForeignKey(User,related_name='+')
#     time = models.DateTimeField(auto_now_add=True)
# 
#     def __unicode__(self):
#         return '' + self.user.get_profile().name + ' follow ' + self.follow.get_profile().name
    
#用户关注了我
# class Fans(models.Model):
#     user = models.ForeignKey(User,related_name='+')
#     fans = models.ForeignKey(User,related_name='+')
#     time = models.DateTimeField(auto_now_add=True)
# 
#     def __unicode__(self):
#         return self.user + ' be fans of ' + self.follow