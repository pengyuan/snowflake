#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import conditional_escape
try:
    from django.utils.encoding import force_unicode
except ImportError: #python3
    # https://docs.djangoproject.com/en/1.5/topics/python3/#string-handling
    from django.utils.encoding import force_text as force_unicode
from django.utils.safestring import mark_safe

STATIC_URL = settings.STATIC_URL.rstrip('/')

class PagedownWidget(forms.Textarea):
    class Media:
        css = {
            'all': ("%s/pagedown/pagedown.css" % STATIC_URL,)
        }
        js = ('%s/pagedown/Markdown.Converter.js' % STATIC_URL,
              '%s/pagedown/Markdown.Sanitizer.js' % STATIC_URL,
              '%s/pagedown/Markdown.Editor.js' % STATIC_URL,
              '%s/pagedown/pagedown_init.js' % STATIC_URL,)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs,name=name)
        final_attrs['class'] += " wmd-input"
        html = [u"""
                <div class="wmd-panel resizable-textarea">
                    <div id="%s_wmd_button_bar"></div>
                    <textarea%s>%s</textarea>
                </div>
            """ % (final_attrs['id'],flatatt(final_attrs),conditional_escape(force_unicode(value)))]
        if settings.WMD_SHOW_PREVIEW:
            html.append(u'<div id="%s_wmd_preview" class="wmd-panel wmd-preview"></div>' % final_attrs['id'])
        return mark_safe(u'\n'.join(html))

class AdminPagedownWidget(admin_widgets.AdminTextareaWidget, PagedownWidget):
#   自定义后台pagedown的css
#     class Media:
#         css = {
#             'all': ("%s/pagedown/pagedown_admin.css" % STATIC_URL,)
#         }
        
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs,name=name)
        final_attrs['class'] += " wmd-input"
        html = [u"""
                <div class="wmd-panel resizable-textarea">
                    <div id="%s_wmd_button_bar"></div>
                    <textarea%s>%s</textarea>
                </div>
            """ % (final_attrs['id'],flatatt(final_attrs),conditional_escape(force_unicode(value)))]
        if settings.WMD_SHOW_PREVIEW:
            html.append(u'<div id="%s_wmd_preview" class="wmd-panel wmd-preview"></div>' % final_attrs['id'])
        return mark_safe(u'\n'.join(html))