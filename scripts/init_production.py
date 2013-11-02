#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.topic.models import Node, ParentNode
from django.contrib.sites.models import Site
from django.core.management import call_command
import MySQLdb
import datetime

conn = MySQLdb.connect(host = 'localhost', user = 'pythonic', passwd = 'pythonic')
cursor = conn.cursor()

try:
    cursor.execute('drop database pythonic')
    cursor.execute('create database if not exists pythonic default charset utf8 COLLATE utf8_general_ci')
    conn.commit()
except Exception, e:
    print e
    conn.rollback()
finally:
    cursor.close()
    conn.close()
    
try:
    call_command('syncdb', interactive=True)
except Exception, e:
    print e
    pass    

conn = MySQLdb.connect(host = 'localhost', user = 'pythonic', passwd = 'pythonic', db='pythonic')
cursor = conn.cursor()
try:
    cursor.execute("use pythonic")
    cursor.execute("ALTER table topic_topic AUTO_INCREMENT=19880929")
    conn.commit()
except Exception, e:
    print e
    conn.rollback()
finally:
    cursor.close()
    conn.close()

#初始化类别
cat_python = ParentNode.objects.create(name=u'Python')
cat_explore = ParentNode.objects.create(name=u'探索')
cat_web = ParentNode.objects.create(name=u'Web开发')
cat_sci = ParentNode.objects.create(name=u'科学计算')
cat_mobile = ParentNode.objects.create(name=u'Mobile')
cat_activity = ParentNode.objects.create(name=u'活动')
#初始化节点
time = datetime.datetime.now()
new_node = Node(name='Pythonic',slug='pythonic',category=cat_python,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='分享',slug='share',category=cat_python,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='奇思妙想',slug='idea',category=cat_python,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='创造',slug='creation',category=cat_python,num_topics=0,created_on=time,updated_on=time)
new_node.save()

new_node = Node(name='瞎扯谈',slug='chat',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='设计',slug='design',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='TED',slug='ted',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='开源',slug='open-source',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Ruby',slug='ruby',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='创业',slug='startup',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Kindle',slug='kindle',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='黑客与画家',slug='kk',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='RESTful',slug='restful',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Rework',slug='rework',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Mac',slug='mac',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Agile',slug='agile',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='测试',slug='testing',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Lisp',slug='lisp',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='翻墙',slug='gfw',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='招聘',slug='job',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()

new_node = Node(name='PyPI',slug='pypi',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='MongoDB',slug='mongodb',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Redis',slug='redis',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='前端开发',slug='front-end',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Web安全',slug='web-security',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='云服务',slug='cloud',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='RabbitMQ',slug='rabbitmq',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='算法',slug='algorithm',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Memcached',slug='memcached',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Git',slug='git',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Database',slug='database',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Linux',slug='linux',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Nginx',slug='nginx',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='运维',slug='operation',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()

new_node = Node(name='机器学习',slug='ml',category=cat_sci,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='可视化',slug='visualization',category=cat_sci,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='OpenStack',slug='openstack',category=cat_sci,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='自然语言处理',slug='nlp',category=cat_sci,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='GUI',slug='gui',category=cat_sci,num_topics=0,created_on=time,updated_on=time)
new_node.save()

new_node = Node(name='iOS',slug='ios',category=cat_mobile,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Android',slug='android',category=cat_mobile,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='HTML5',slug='html5',category=cat_mobile,num_topics=0,created_on=time,updated_on=time)
new_node.save()

new_node = Node(name='线下活动',slug='activity',category=cat_activity,num_topics=0,created_on=time,updated_on=time)
new_node.save()

Site.objects.filter(id=1).update(domain='pythonic.org',name='Pythonic社区')