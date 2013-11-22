#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.accounts.function import gfm
from apps.people.models import Notice, Message
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.template.defaultfilters import timesince as _timesince
from django.utils.timezone import LocalTimezone
import datetime
import logging
import markdown2


register = template.Library()   
#just a demo
@register.filter('hello')   
def hello(value,msg="Hello"):   
    return "%s,%s！" % (msg,value)   

# @register.filter
# def time_since(d, now=None):
#     # Convert datetime.date to datetime.datetime for comparison.
#     if not d:
#         return ''
#     if not isinstance(d, datetime.datetime):
#         d = datetime.datetime(d.year, d.month, d.day)
#     if now and not isinstance(now, datetime.datetime):
#         now = datetime.datetime(now.year, now.month, now.day)
#     if not now:
#         if d.tzinfo:
#             now = datetime.datetime.now(LocalTimezone(d))
#         else:
#             now = datetime.datetime.now()
#     # ignore microsecond part of 'd' since we removed it from 'now'
#     delta = now - (d - datetime.timedelta(0, 0, d.microsecond))
#     since = delta.days * 24 * 60 * 60 + delta.seconds
#     if since // (60 * 60 * 24) < 3:
#         return _("%s ago") % _timesince(d)
#     return _date(d, "Y-m-d H:i")


@register.filter
def time_since(value):
    #logging.error(value)
    now = datetime.datetime.now()
    try:
        difference = now - value
    except:
        return value
    if difference <= datetime.timedelta(minutes=1):
        return '刚刚'
    #logging.error(timesince(value)+'   '+timesince(value).split(', ')[0])
    return _timesince(value).split(', ')[0]+'前'

@register.filter
def adjust_link(value):
    if value.startswith('http://') or value.startswith('https://'):
        return value
    else:
        return 'http://'+value

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
    #return gfm.markdown(value)
    return mark_safe(markdown2.markdown(gfm(value)))

@register.filter
def count_thanks(thanks):
    for item in thanks.all():
        print item

@register.filter
def thanks_list(thanks):
    thanks = thanks.all()[:3]
    html = ''
    for item in thanks:
        html += '<a href="/people/'+item.get_profile().slug+'">'+item.get_profile().name+'</a>、'
    html = html[:-1] + u' 赞同'
    return html
thanks_list.is_safe = True 