#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.site.forms import FeedbackForm
from apps.topic.models import Topic, Node, ParentNode
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.aggregates import Count
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
import datetime

def index(request):
    context = {}
    topic_list = Topic.objects.all().order_by('-updated_on')[:41]
    if topic_list.count() == 41:
        more = True
    else:
        more = False
    context['topics'] = topic_list[:40]
    context['more'] = more
    all_nodes = []
    parent_nodes = ParentNode.objects.all()
    for item in parent_nodes:
        node = {}
        children_nodes = Node.objects.filter(category=item.id)
        node['parent'] = item.name
        node['nodes'] = children_nodes
        all_nodes.append(node)
    context['all_nodes'] = all_nodes
    time_now = datetime.datetime.now()
    from_date = time_now - datetime.timedelta(days=30)
    hot_topics = Topic.objects.filter(created_on__range=[from_date, time_now]).order_by('-num_replies')[:10]
    context['hot_topics'] = hot_topics
    hot_nodes = Node.objects.filter(num_topics__gt=0,updated_on__gt=from_date).order_by('-updated_on')[:10]
    context['hot_nodes'] = hot_nodes
    return render(request,'index.html',context)

def star(request):
    context = {}
    time_now = datetime.datetime.now()
    from_date = time_now - datetime.timedelta(days=7)
    hot_topics = Topic.objects.filter(created_on__range=[from_date, time_now]).order_by('-num_replies')[:10]
    context['hot_topics'] = hot_topics
    hot_nodes = Node.objects.filter(num_topics__gt=0,updated_on__gt=from_date).order_by('-updated_on')[:10]
    context['hot_nodes'] = hot_nodes
    
    from_date2 = time_now - datetime.timedelta(days=30)
    topic_list = Topic.objects.filter(updated_on__range=[from_date2, time_now],likes__isnull=False).annotate(likes_count=Count('likes')).order_by('-likes_count')[:40]
    
    context['topics'] = topic_list
    
    all_nodes = []
    parent_nodes = ParentNode.objects.all()
    for item in parent_nodes:
        node = {}
        children_nodes = Node.objects.filter(category=item.id)
        node['parent'] = item.name
        node['nodes'] = children_nodes
        all_nodes.append(node)
    context['all_nodes'] = all_nodes
    
    return render(request,'star.html',context)

def recent(request):
    context = {}
    topic_list = Topic.objects.all().order_by('-updated_on')
    paginator = Paginator(topic_list, 5)

    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    context['topics'] = topics
    return render(request,'recent.html',context)

def about(request):
    return render(request,'about.html')

def zen(request):
    return render(request,'zen.html')

def feedback(request):
    if request.method == 'GET':
        context = {}
        form = FeedbackForm()
        context['form'] = form
        return render(request,'feedback.html',context)
    form = FeedbackForm(request.POST)
    if form.is_valid():
        feedback = form.save(commit=False)
        if request.user.is_authenticated():
            feedback.author = request.user
        else:
            feedback.author = None
        feedback.save()
    return HttpResponseRedirect('/feedback/success')

def feedback_success(request):
    return render(request,'feedback_success.html')

def help_use(request):
    return render(request,'help.html')

def one(request):
    return render(request,'one.html')

def people(request):
    context = {}
    peoples = User.objects.filter(is_active=True).order_by('date_joined')
    paginator = Paginator(peoples, 100)
    page = request.GET.get('page')
    try:
        people_list = paginator.page(page)
    except PageNotAnInteger:
        people_list = paginator.page(1)
    except EmptyPage:
        people_list = paginator.page(paginator.num_pages)
    context['people_list'] = people_list
    context['manage_list'] = User.objects.filter(is_active=True,is_staff=True).order_by('date_joined')
    return render(request,'people_list.html',context)