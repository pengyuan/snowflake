#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.accounts.models import UserProfile
from apps.people.models import Message, Notice
from apps.topic.forms import MessageForm, MessageReply
from apps.topic.models import Topic, Reply
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from django.http.response import HttpResponse, HttpResponseServerError, \
    HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils import simplejson
from django.utils.timesince import timesince
import datetime
import re

def home(request, user_slug):
    context = {}
    if request.method == 'POST':
        return render(request,'index.html',locals())
    try:
        user_profile = UserProfile.objects.get(slug=user_slug)
    except UserProfile.DoesNotExist:
        raise Http404
    topic_list = Topic.objects.filter(author=user_profile.user).annotate(likes_count=Count('likes')).order_by('-likes_count','-created_on')[:10]
    if request.user.is_authenticated(): 
        num_private_message = Message.objects.filter(belong_to=request.user,talk_to=user_profile.user,is_deleted=False).count()
        context['num_private_message'] = num_private_message
    context['people'] = user_profile.user
    context['topic_list'] = topic_list
    return render(request,'people.html',context)

def reply(request, user_slug):
    context = {}
    if request.method == 'POST':
        return render(request,'index.html',locals())
    try:
        user_profile = UserProfile.objects.get(slug=user_slug)
    except UserProfile.DoesNotExist:
        raise Http404
    reply_list = Reply.objects.filter(author=user_profile.user).order_by('-created_on')[:10]
    if request.user.is_authenticated(): 
        num_private_message = Message.objects.filter(belong_to=request.user,talk_to=user_profile.user,is_deleted=False).count()
        context['num_private_message'] = num_private_message
    context['people'] = user_profile.user
    context['reply_list'] = reply_list
    return render(request,'people_reply.html',context)

def thank(request, user_slug):
    context = {}
    if request.method == 'POST':
        return render(request,'index.html',locals())
    try:
        user_profile = UserProfile.objects.get(slug=user_slug)
    except UserProfile.DoesNotExist:
        raise Http404
    thank_list = Reply.objects.filter(author=user_profile.user,thanks__isnull=False).annotate(thanks_count=Count('thanks')).order_by('-thanks_count')[:10]
    #thank_list = sorted(thank_list, key=lambda x: x.thanks.all().count(), reverse=True)
    if request.user.is_authenticated(): 
        num_private_message = Message.objects.filter(belong_to=request.user,talk_to=user_profile.user,is_deleted=False).count()
        context['num_private_message'] = num_private_message
    context['people'] = user_profile.user
    context['thank_list'] = thank_list
    return render(request,'people_thank.html',context)

def like(request, user_slug):
    context = {}
    if request.method == 'POST':
        return render(request,'index.html',locals())
    try:
        user_profile = UserProfile.objects.get(slug=user_slug)
    except UserProfile.DoesNotExist:
        raise Http404
    like_list =  user_profile.user.topic_set.all().order_by('-updated_on')[:10]
    if request.user.is_authenticated(): 
        num_private_message = Message.objects.filter(belong_to=request.user,talk_to=user_profile.user,is_deleted=False).count()
        context['num_private_message'] = num_private_message
    context['people'] = user_profile.user
    context['like_list'] = like_list
    return render(request,'people_like.html',context)

@login_required
def notice(request):
    context = {}
    if request.method == 'GET':
        notice_list = Notice.objects.filter(recipient=request.user).order_by('-time')
        num_notice = notice_list.filter(is_readed=False).count()
        talk_list = Message.objects.filter(belong_to=request.user).values('talk_to').distinct()
        num_message = 0
        if talk_list: 
            for item in talk_list:
                num = Message.objects.filter(is_sender=False,belong_to=request.user,talk_to=item['talk_to'],is_readed=False,is_deleted=False).count()
                num_message += num
        context['num_notice'] = num_notice
        context['num_message'] = num_message
        context['notice_list'] = notice_list
        return render(request,'notice.html',context)

@login_required
def notice_mark(request):
    if request.method == 'GET':
        Notice.objects.filter(recipient=request.user,is_readed=False).update(is_readed=True)
        return HttpResponseRedirect('/notice')
    
@login_required
def message(request):
    if request.method =='GET':
        context = {}
        num_notice = Notice.objects.filter(recipient=request.user,is_readed=False).count()
        talk_list = Message.objects.filter(belong_to=request.user).values('talk_to').distinct()
        msg_list = []
        num_message = 0
        if talk_list: 
            for item in talk_list:
                message = Message.objects.filter(belong_to=request.user,talk_to=item['talk_to'],is_deleted=False).order_by('-time')[0]
                num = Message.objects.filter(is_sender=False,belong_to=request.user,talk_to=item['talk_to'],is_readed=False,is_deleted=False).count()
                num_message += num
                item = {}
                item['message'] = message
                item['number'] = num
                msg_list.append(item)
        context['num_notice'] = num_notice
        context['num_message'] = num_message
        context['msg_list'] = sorted(msg_list, key=lambda x:x['message'].time, reverse=True)
        
        return render(request,'message.html',context)

@login_required
def message_create(request):
    if request.method =='GET':
        context = {}
        num_notice = Notice.objects.filter(recipient=request.user,is_readed=False).count()
        talk_list = Message.objects.filter(belong_to=request.user).values('talk_to').distinct()
        num_message = 0
        if talk_list: 
            for item in talk_list:
                num = Message.objects.filter(is_sender=False,belong_to=request.user,talk_to=item['talk_to'],is_readed=False,is_deleted=False).count()
                num_message += num
        context['num_notice'] = num_notice
        context['num_message'] = num_message
        form = MessageForm()
        context['form'] = form
        return render(request,'message_new.html',context)    
    form = MessageForm(request.POST)
    if form.is_valid():
        talk_to_name = form.cleaned_data['recipient']
        content = form.cleaned_data['content']
        try:
            talk_to_profile = UserProfile.objects.get(name=talk_to_name)
        except UserProfile.DoesNotExist:
            messages.error(request,'该用户不存在')
            pass
        else:
            talk_to = talk_to_profile.user
            sender = request.user
            if sender.id == talk_to.id:
                messages.error(request,'不能发私信给自己')
                return HttpResponseRedirect('/message_new')
            else:
                time = datetime.datetime.now()
                Message.objects.create(is_sender=True,talk_to=talk_to,belong_to=request.user,content=content,time=time,is_readed=True)
                Message.objects.create(is_sender=False,talk_to=request.user,belong_to=talk_to,content=content,time=time)
                return HttpResponseRedirect('/message')
    else:
        return render(request,'message_new.html',locals())

@login_required
def message_history(request,talk_to):
    context = {}
    try:
        talk_to_profile = UserProfile.objects.get(slug=talk_to)
    except UserProfile.DoesNotExist:
        raise Http404
    if request.method =='GET':
        Message.objects.filter(is_sender=False,talk_to=talk_to_profile.user,belong_to=request.user,is_readed=False,is_deleted=False).update(is_readed=True) 
        msg_list = Message.objects.filter(belong_to=request.user,talk_to=talk_to_profile.user,is_deleted=False).order_by('-time')[:5]
        #my_queryset.reverse()[:5]
        context['form'] = MessageReply()
        context['msg_list'] = msg_list
#         try:
#             talk_to = User.objects.get(pk=talk_to)
#         except:
#             talk_to = None
        context['talk_to'] = talk_to_profile.user
        return render(request,'message_history.html',context)

@login_required
def ajax_message(request):
    success = False
    to_return = {'msg':u'No GET data sent.'}
    if request.method =='GET':
        num = request.GET['num_message']
        end = int(num) + 10
        talk_to = request.GET['to_message']
        msg_list = Message.objects.filter(belong_to=request.user,talk_to=talk_to,is_deleted=False).order_by('-time')[num:end+1]
        if msg_list.count()==11:
            to_return['check'] = True
        else:
            to_return['check'] = False
        msgs = []
        for item in msg_list[:10]:
            msg = {}
            msg['id'] = item.id
            msg['is_sender'] = item.is_sender
            msg['belong_to'] = item.belong_to.get_profile().slug
            msg['belong_to_avatar'] = item.belong_to.get_profile().avatar
            msg['talk_to'] = item.talk_to.get_profile().slug
            msg['talk_to_avatar'] = item.talk_to.get_profile().avatar
            msg['content'] = item.content
            msg['time'] = timesince(item.time).split(', ')[0]+'前'
            msgs.append(msg)
        to_return['msgs'] = msgs
        to_return['end'] = end
        
        success = True
    #serialized = serializers.serialize("json",msg_list,ensure_ascii=False) #, fields=('foo','bar')
    serialized = simplejson.dumps(to_return)
    if success == True:
        return HttpResponse(serialized, mimetype="application/json")
    else:
        return HttpResponseServerError(serialized, mimetype="application/json")
  
@login_required
def message_reply(request):
    if request.method =='POST':
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/')
        form = MessageReply(request.POST)
        talk_to = request.POST['talk_to']
        if form.is_valid():
            
            content = form.cleaned_data['content']
            try:
                talk_to = User.objects.get(pk=talk_to,is_active=True)
            except User.DoesNotExist:
                messages.error(request,'该用户不存在或已注销')
                pass
            else:
                time = datetime.datetime.now()
                Message.objects.create(is_sender=True,talk_to=talk_to,belong_to=request.user,content=content,time=time,is_readed=True)
                Message.objects.create(is_sender=False,talk_to=request.user,belong_to=talk_to,content=content,time=time)
            return HttpResponseRedirect('/message/'+talk_to.get_profile().slug+'/')
        else:
            Message.objects.filter(is_sender=False,talk_to=talk_to,belong_to=request.user,is_readed=False,is_deleted=False).update(is_readed=True) 
            msg_list = Message.objects.filter(belong_to=request.user,talk_to=talk_to,is_deleted=False).order_by('time')[:20]
            try:
                talk_to = User.objects.get(pk=talk_to,is_active=True)
            except:
                talk_to = None
            return render(request,'message_history.html',locals())
    return HttpResponseRedirect('/')

def ajax_user_match(request):
    success = False
    to_return = {'msg':u'No POST data sent.' }
    if request.method == "GET":
        get = request.GET.copy()
        if get.has_key('q'):
            q = get['q'].strip()
            qs = re.split(r'\s+',q)
            match_list = []
            profiles = UserProfile.objects
            for item in qs:
                profiles = profiles.filter(name__icontains=item)
            profiles = profiles[0:10]
            if profiles:
                for item in profiles:
                    user = {}
                    user['avatar'] = item.avatar
                    user['name'] = item.name
                    user['signature'] = item.signature
                    match_list.append(user)        
            to_return["match"] = match_list
            success = True
        else:
            to_return['msg'] = u"Require keywords"
    serialized = simplejson.dumps(to_return)
    if success == True:
        return HttpResponse(serialized, mimetype="application/json")
    else:
        return HttpResponseServerError(serialized, mimetype="application/json")

# @login_required
# def ajax_focus(request):
#     success = False
#     to_return = {}
#     if request.method =='GET':
#         get = request.GET.copy()
#         if get.has_key('people_id'):
#             people_id = get['people_id']
#             try:
#                 user = User.objects.get(pk=people_id)
#             except User.DoesNotExist:
#                 raise Http404
#             follow = Follow.objects.create(user=request.user,follow=user)
#             to_return['result'] = True
#             success=True
#         else:
#             to_return={'msg':u'Require keywords'}
#     serialized = simplejson.dumps(to_return)
#     if success:
#         return HttpResponse(serialized, mimetype="application/json")
#     else:
#         return HttpResponseServerError(serialized, mimetype="application/json")

# def cancel_focus(request, node_id):
#     if request.method =='GET':
#         node = Node.objects.get(pk=node_id)
#         node.users.remove(request.user)
#     return HttpResponseRedirect('/node/'+node_id+"/")