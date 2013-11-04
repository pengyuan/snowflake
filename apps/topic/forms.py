#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.pagedown.widgets import PagedownWidget
from apps.topic.models import Topic, Reply, Node
from apps.topic.widgets import MarkDownInput
from django import forms

class TopicForm(forms.ModelForm):
    title = forms.CharField(label=u'标题',widget=forms.TextInput(attrs={'class':'span12'}))
    #content = forms.CharField(label=u'内容',widget=forms.Textarea(attrs={'class':'span12'}))
    #content = forms.CharField(label=u'内容',widget=MarkDownInput(attrs={'class':'span12 resizable','style':'opacity: 1; height: 179px;'}))
    content = forms.CharField(widget=PagedownWidget())   
    class Meta:
        model = Topic
        fields = ('title','content')#$("#count_char").hide(5000);
        
class ReplyForm(forms.ModelForm):
    #content = forms.CharField(label=u'回复',widget=forms.Textarea(attrs={'class':'span12 resizable'}))
    #content = forms.CharField(label=u'内容',widget=MarkDownInput(attrs={'class':'span12 resizable','style':'opacity: 1; height: 179px;'}))
    content = forms.CharField(widget=PagedownWidget()) 
    class Meta:
        model = Reply
        fields = ('content',)
        
class MessageForm(forms.Form):
    recipient = forms.CharField(label=u'发给',max_length=20,widget=forms.TextInput(attrs={'class':'span3','autocomplete':'off','placeholder':'搜索居民'}))
    content = forms.CharField(label=u'内容',max_length=200,widget=forms.Textarea(attrs={'class':'span8','style':'height:100px;'}))

class MessageReply(forms.Form):
    content = forms.CharField(label=u'回复',max_length=200,widget=forms.Textarea(attrs={'id':'message_reply','class':'span12','style':'height:100px;','onkeyup':'words_deal("#message_reply",200);'}))
    
class ApplyForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ('name',)

class NodeEditForm(forms.Form):
    #content = forms.CharField(label=u'添加新描述',widget=forms.Textarea(attrs={'class':'span12'}))
    content = forms.CharField(label=u'添加新描述',widget=MarkDownInput())