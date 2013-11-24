#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.people.models import Notice, Message
from apps.topic.gfm import gfm
from datetime import datetime
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
register = template.Library()   
#just a demo
@register.filter('hello')   
def hello(value,msg="Hello"):   
    return "%s,%s！" % (msg,value)   

@register.filter(name='timesince_human')
def humanize_timesince(date):
    delta = datetime.now() - date

    num_years = delta.days / 365
    if (num_years > 0):
        return date.strftime("%Y-%m-%d %H:%I:%S")

#     num_weeks = delta.days / 7
#     if (num_weeks > 0):
#         return ungettext(u"%d week ago", u"%d weeks ago", num_weeks) % num_weeks

    if (delta.days > 0):
        return u"%d天前" % delta.days

    num_hours = delta.seconds / 3600
    if (num_hours > 0):
        return u"%d小时前" % num_hours

    num_minutes = delta.seconds / 60
    if (num_minutes > 0):
        return u"%d分钟前" % num_minutes

    return u"刚刚"

# @register.filter
# @stringfilter
# def upto(value, delimiter=None):
#     return value.split(delimiter)[0]+u'前'
# upto.is_safe = True
# 
# @register.filter
# def time_since(value):
#     now = datetime.now()
#     try:
#         difference = now - value
#     except:
#         return value
# 
#     if difference <= timedelta(minutes=1):
#         return '刚刚'
#     return '%(time)s前' % {'time': timesince(value)}

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
    return mark_safe(gfm(value))
    #return mark_safe(markdown2.markdown(gfm(value)))
# 
# @register.filter
# def count_thanks(thanks):
#     for item in thanks.all():
#         print item

@register.filter
def thanks_list(thanks):
    thanks = thanks.all()[:3]
    html = ''
    for item in thanks:
        html += '<a href="/people/'+item.get_profile().slug+'">'+item.get_profile().name+'</a>、'
    html = html[:-1] + u' 赞同'
    return html
thanks_list.is_safe = True 