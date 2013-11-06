#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.pagedown.widgets import PagedownWidget
from apps.topic.models import Topic, Reply, Node
from django import forms

class TopicForm(forms.ModelForm):
    title = forms.CharField(label=u'标题',widget=forms.TextInput(attrs={'class':'span12'}))
    content = forms.CharField(label=u'内容',max_length=1000,widget=PagedownWidget(attrs={'id':'topic_form','class':'span12 resizable','style':'opacity: 1; height: 180px;','onkeyup':'words_deal("#topic_form",1000);'}))   
    class Meta:
        model = Topic
        fields = ('title','content')
        
class ReplyForm(forms.ModelForm):
    content = forms.CharField(max_length=1000,widget=PagedownWidget(attrs={'id':'reply_form','class':'span12 resizable','style':'opacity: 1; height: 180px;','onkeyup':'words_deal("#reply_form",1000);'})) 
    class Meta:
        model = Reply
        fields = ('content',)
        
class MessageForm(forms.Form):
    recipient = forms.CharField(label=u'发给',max_length=20,widget=forms.TextInput(attrs={'class':'span6','autocomplete':'off','placeholder':'搜索居民'}))
    content = forms.CharField(label=u'内容',max_length=200,widget=forms.Textarea(attrs={'class':'span12','style':'height:100px;'}))

class MessageReply(forms.Form):
    content = forms.CharField(label=u'回复',max_length=200,widget=forms.Textarea(attrs={'id':'message_reply','class':'span12','style':'height:100px;','onkeyup':'words_deal("#message_reply",200);'}))
    
class ApplyForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ('name',)

class NodeEditForm(forms.Form):
    content = forms.CharField(label=u'内容',max_length=1000,widget=PagedownWidget(attrs={'id':'node_form','class':'span12 resizable','style':'opacity: 1; height: 180px;','onkeyup':'words_deal("#node_form",1000);'}))   