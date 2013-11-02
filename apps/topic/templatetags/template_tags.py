#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.people.models import Notice, Message
from apps.topic.templatetags import markdown2
from datetime import datetime, timedelta
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.timesince import timesince
register = template.Library()   

#just a demo
@register.filter('hello')   
def hello(value,msg="Hello"):   
    return "%s,%s！" % (msg,value)   

@register.filter
def time_since(value):
    now = datetime.now()
    try:
        difference = now - value
    except:
        return value

    if difference <= timedelta(minutes=1):
        return '刚刚'
    return '%(time)s前' % {'time': timesince(value).split(', ')[0]}

@register.simple_tag
def num_message(user):
    num_notice = Notice.objects.filter(recipient=user,is_readed=False).count()
    num_pm = Message.objects.filter(is_sender=False,belong_to=user,is_readed=False,is_deleted=False).count()
    num = num_notice + num_pm
    if num == 0:
        return ''
    else:
        return "<span class='num'>"+ str(num) +"</span>"

@register.filter(is_safe=True)
@stringfilter
def markdown2html(value):
    return mark_safe(markdown2.markdown(value,safe_mode=True))