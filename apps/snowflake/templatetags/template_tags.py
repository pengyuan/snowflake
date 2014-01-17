#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.snowflake.utils import gfm
from apps.snowflake.views import Notice
from django import template
from django.template.defaultfilters import stringfilter
from django.utils import timezone
from django.utils.safestring import mark_safe
import hashlib
import urllib
register = template.Library()   

@register.simple_tag
def timesince_human(date):
    delta = timezone.now() - date
    num_years = delta.days / 365
    if (num_years > 0):
        return date.strftime("%Y-%m-%d %H:%I:%S")
    if (delta.days > 0):
        return u"%d 天前" % delta.days
    num_hours = delta.seconds / 3600
    if (num_hours > 0):
        return u"%d 小时前" % num_hours
    num_minutes = delta.seconds / 60
    if (num_minutes > 0):
        return u"%d 分钟前" % num_minutes
    return u"刚刚"


@register.filter
def adjust_link(value):
    if value.startswith('http://') or value.startswith('https://'):
        return value
    else:
        return 'http://'+value


@register.simple_tag
def num_notice(user):
    num = Notice.objects.filter(to_user=user,is_readed=False,is_deleted=False).count()
    if num == 0:
        return ''
    else:
        return "<span class='num'>"+ str(num) +"</span>"


@register.simple_tag
def notice_set_all_readed(user):
    Notice.objects.filter(to_user=user,is_readed=False,is_deleted=False).update(is_readed=True)
    return ''


@register.filter(is_safe=True)
@stringfilter
def markdown2html(value):
    return mark_safe(gfm(value))


class gravatar_url_node(template.Node):
    def __init__(self, email, size):
        self.email = template.Variable(email)
        self.size = size
  
    def render(self, context):
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ''
  
        default = "mm"
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(self.size)})
  
        return gravatar_url
  
@register.tag
def gravatar_url(parser, token):
    data = token.split_contents()
    length = len(data)
    if length < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % token.contents.split()[0]
    elif length == 2:
        size = 40
    else:
        size = token.split_contents()[2]
    email = token.split_contents()[1]    
    return gravatar_url_node(email, size)