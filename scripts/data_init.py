#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.accounts.models import User
from apps.snowflake.models import Category, Node, Topic
from django.core.management import call_command
from django.utils import timezone
import time

USER_DATA = [
        {'username':'a@gmail.com','password':'123456','name':'Eric','city':u'武汉'},
        {'username':'b@gmail.com','password':'123456','name':'Jack','city':u'北京'},
        {'username':'c@gmail.com','password':'123456','name':'Robbin','city':u'杭州'},
        {'username':'d@gmail.com','password':'123456','name':'William','city':u'深圳'}
]

CATEGORY_DATA = [
        {'name':'Python'},
        {'name':u'探索'},
        {'name':u'Web开发'},
        {'name':u'科学计算'},
        {'name':u'活动'}
]

NODE_DATA = [
        {'name':'Pythonic','slug':'pythonic','parent':'Python'},
        {'name':u'分享','slug':'share','parent':'Python'},
        {'name':u'奇思妙想','slug':'idea','parent':'Python'},
        {'name':u'创造','slug':'creation','parent':'Python'},
        
        {'name':u'瞎扯谈','slug':'chat','parent':u'探索'},
        {'name':u'设计','slug':'design','parent':u'探索'},
        {'name':'TED','slug':'ted','parent':u'探索'},
        {'name':u'开源','slug':'open-source','parent':u'探索'},
        {'name':u'创业','slug':'startup','parent':u'探索'},
        {'name':'Kindle','slug':'kindle','parent':u'探索'},
        {'name':u'黑客与画家','slug':'kk','parent':u'探索'},
        {'name':'Rework','slug':'rework','parent':u'探索'},
        {'name':'Lisp','slug':'lisp','parent':u'探索'},
        
        {'name':'PyPI','slug':'pypi','parent':u'Web开发'},
        {'name':'MongoDB','slug':'mongodb','parent':u'Web开发'},
        {'name':'Redis','slug':'redis','parent':u'Web开发'},
        {'name':u'前端开发','slug':'front-end','parent':u'Web开发'},
        {'name':u'云服务','slug':'cloud','parent':u'Web开发'},
        {'name':u'算法','slug':'algorithm','parent':u'Web开发'},
        {'name':'Git','slug':'git','parent':u'Web开发'},

        
        {'name':u'机器学习','slug':'ml','parent':u'科学计算'},
        {'name':'OpenStack','slug':'openstack','parent':u'科学计算'},
        {'name':u'自然语言处理','slug':'nlp','parent':u'科学计算'},

        {'name':u'线下活动','slug':'activity','parent':u'活动'},
]

TOPIC_DATA = [
        {'node':'Pythonic','author':'Eric','title':u'Snowflake测试','content':u'Snowflake是一个简单的论坛。基于信息流和节点组织内容。'}
]



try:
    call_command('syncdb', interactive=True)
except Exception, e:
    print "syncdb operation failure", "\n", e.args[0]
    pass

for item in USER_DATA:
    user = User.objects.create_user(username=item['username'],password=item['password'],name=item['name'],city=item['city'])

for item in CATEGORY_DATA:
    parent_node = Category.objects.create(name=item['name'])
    parent_node.save()

for item in NODE_DATA:
    category = Category.objects.filter(name=item['parent'])[0]
    time = timezone.now()
    node = Node.objects.create(name=item['name'],slug=item['slug'],category=category,updated_on=time)
    node.save()
    
for item in TOPIC_DATA:
    node = Node.objects.filter(name=item['node'])[0]
    user = User.objects.filter(name=item['author'])[0]
    time = timezone.now()
    topic = Topic.objects.create(node=node,author=user,title=item['title'],content=item['content'],last_reply = user,updated_on = time)
    topic.save()
    node.num_topics = node.num_topics + 1
    node.updated_on = time
    node.save()