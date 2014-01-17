#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.accounts.models import User
from apps.snowflake.forms import ReplyForm, TopicForm, EditForm
from apps.snowflake.models import Topic, Reply, Description, Category, Node, \
    Notice
from apps.snowflake.utils import hot_function
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, Http404
from django.http.response import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.utils import timezone
from settings import NUM_TOPICS_PER_PAGE, NUM_REPLIES_PER_PAGE
import json

# homepage
def index(request):
    context = {}
    topics = Topic.objects.all().order_by('-updated_on')[:NUM_TOPICS_PER_PAGE]
    context['topics'] = topics
    
    nodes = []
    categories = Category.objects.all()
    for item in categories:
        node = {}
        category_nodes = Node.objects.filter(category=item.id)
        node['category_name'] = item.name
        node['category_nodes'] = category_nodes
        nodes.append(node)
    context['nodes'] = nodes
    
    active_users = User.objects.all().order_by('-date_joined')[:20]
    context['active_users'] = active_users
    
    new_replies = Reply.objects.all().order_by('-created_on')[:5]
    context['new_replies'] = new_replies
    
    from_date = timezone.now() - timezone.timedelta(days=7)
    hot_nodes = Node.objects.filter(num_topics__gt=0,updated_on__gt=from_date).order_by('num_topics')[:10]
    context['hot_nodes'] = hot_nodes
    
    return render(request,'index.html',context)


# recent topics
def recent(request):
    context = {}
    topic_list = Topic.objects.all().order_by('-updated_on')
    paginator = Paginator(topic_list, NUM_TOPICS_PER_PAGE)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    context['topics'] = topics
    
    nodes = []
    categories = Category.objects.all()
    for item in categories:
        node = {}
        category_nodes = Node.objects.filter(category=item.id)
        node['category_name'] = item.name
        node['category_nodes'] = category_nodes
        nodes.append(node)
    context['nodes'] = nodes
    
    active_users = User.objects.all().order_by('-date_joined')[:20]
    context['active_users'] = active_users
    
    new_replies = Reply.objects.all().order_by('-created_on')[:5]
    context['new_replies'] = new_replies
    
    from_date = timezone.now() - timezone.timedelta(days=7)
    hot_nodes = Node.objects.filter(num_topics__gt=0,updated_on__gt=from_date).order_by('num_topics')[:10]
    context['hot_nodes'] = hot_nodes
    
    return render(request,'recent.html',context)


# hot topics
def hot(request):
    context = {}
    time_now = timezone.now()
    from_date = time_now - timezone.timedelta(days=30)
    hot_topics = Topic.objects.filter(created_on__range=[from_date, time_now])
    hot_topics = sorted(hot_topics, key=lambda x: hot_function(x), reverse=True)
    context['hot_topics'] = hot_topics[:20]
    
    return render(request,'hot.html',context)


# show topics related to a node
def node(request, node_slug):
    context = {}
    try:
        node = Node.objects.get(slug=node_slug)
    except Node.DoesNotExist:
        raise Http404
    context['node'] = node
    
    description = Description.objects.filter(node=node,active=True)
    if description:
        description = description[0]
    else:
        description = None
    context['description'] = description
  
    all_topics = Topic.objects.filter(node=node).order_by('-updated_on')
    paginator = Paginator(all_topics, NUM_TOPICS_PER_PAGE)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)  
    context['topics'] = topics
    
    context['relative_nodes'] = Node.objects.filter(category=node.category).order_by('num_topics')
    context['form'] = TopicForm()
    
    return render(request,'node.html',context)


@login_required
def new(request, node_slug):
    print 'aaa'
    context = {}
    try:
        node = Node.objects.get(slug=node_slug)
    except Node.DoesNotExist:
        print node_slug,'hehehh'
        raise Http404
    
    if request.method == 'GET':
        form = TopicForm()
        context['node'] = node
        context['form'] = form
        return render(request,'new.html',context)
    
    form = TopicForm(request.POST)
    if form.is_valid():
        topic = form.save(commit=False)
        topic.node = node
        topic.author = request.user
        topic.last_reply = request.user
        topic.updated_on = timezone.now()
        topic.save()
        node.num_topics += 1
        node.save()
        
    return HttpResponseRedirect('/node/'+node_slug)


@login_required
def edit(request,node_slug):
    context = {}
    try:
        node = Node.objects.get(slug=node_slug)
    except Node.DoesNotExist:
        raise Http404
    
    if request.method == 'GET':
        description = Description.objects.filter(node=node).order_by('-time')
        context['node'] = node
        context['description'] = description
        context['form'] = EditForm()
        return render(request,'edit.html',context)
    
    form = EditForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data['content']
        Description.objects.filter(node=node).update(active=False)
        Description.objects.create(content=content,author=request.user,node=node,active=True)
        
    return HttpResponseRedirect('/node/'+node_slug)


@login_required
def choose(request,node_slug):
    if request.method == 'GET':
        return HttpResponseRedirect('/node/'+node_slug)
    
    try:
        node = Node.objects.get(slug=node_slug)
    except Node.DoesNotExist:
        raise Http404
    
    description_id = request.POST['description_id']    
    try:
        description = Description.objects.get(id=description_id)
    except Description.DoesNotExist:
        raise Http404
    
    if description.node == node:
        Description.objects.filter(node=node).update(active=False)
        description.active = True
        description.save()
    else:
        raise Http404
    
    return HttpResponseRedirect('/node/'+node_slug)


# topic page
def topic(request,topic_id):
    context = {}
    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        raise Http404
    topic.num_views += 1
    topic.save()
    
    replys_all = Reply.objects.filter(topic=topic).order_by('created_on')
    paginator = Paginator(replys_all, NUM_REPLIES_PER_PAGE)
    page = request.GET.get('page')
    try:
        replys = paginator.page(page)
    except PageNotAnInteger:
        replys = paginator.page(1)
    except EmptyPage:
        replys = paginator.page(paginator.num_pages)
            
    description = Description.objects.filter(node=topic.node,active=True)
    if description:
        description = description[0]
    else:
        description = None
        
    context['description'] = description
    context['topic'] = topic
    context['node'] = topic.node
    context['replys'] = replys
    context['form'] = ReplyForm()
    
    return render(request,'topic.html',context)



@login_required
def reply(request, topic_id):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            try:
                topic = Topic.objects.get(id=topic_id)
            except Topic.DoesNotExist:
                raise Http404
            reply.topic = topic
            reply.save()
            
            topic.num_replies += 1
            topic.updated_on = timezone.now()
            topic.last_reply = request.user
            topic.save()
            
            paginator = Paginator(Reply.objects.filter(topic=topic).order_by('created_on'), NUM_REPLIES_PER_PAGE)    
                    
    return HttpResponseRedirect('/topic/'+topic_id+'?page='+str(paginator.num_pages)+'#reply')


@login_required
def ajax_thank(request):
    print 'here'
    success = False
    to_return = {'msg':u'No GET data sent.' }
    
    if request.method == "GET":
        get = request.GET.copy()
        if get.has_key('reply_id'):
            reply_id = get['reply_id'].strip()
            try:
                reply = Reply.objects.get(id=reply_id)
            except Reply.DoesNotExist:
                raise Http404
            user = request.user
            print 'a'
            if not user in reply.thank_set.all():
                reply.thank_set.add(user)
                to_return['check'] = True
            else:
                to_return['check'] = False
            print 'b'
            to_return['count'] = reply.thank_set.all().count()
            success = True
        else:
            to_return['msg'] = u"Require keywords"
    print 'c'
    serialized = json.dumps(to_return)
    print 'd'
    print serialized
    if success == True:
        return HttpResponse(serialized, content_type="application/json")
    else:
        return HttpResponseServerError(serialized, content_type="application/json")


def home(request, user_name):
    context = {}
    if request.method == 'POST':
        return render(request,'index.html',locals())
    try:
        user = User.objects.get(name=user_name)
    except User.DoesNotExist:
        raise Http404
    topics = Topic.objects.filter(author=user).order_by('-created_on')[:10]
    replys = Reply.objects.filter(author=user).order_by('-created_on')[:10]

    context['people'] = user
    context['topics'] = topics
    context['replys'] = replys
    
    return render(request,'home.html',context)


@login_required
def notice(request):
    context = {}
    if request.method == 'GET':
        notices = Notice.objects.filter(to_user=request.user,is_deleted=False).order_by('-time')
        context['notices'] = notices
        
        return render(request,'notice.html',context)

@login_required
def delete(request, notice_id):
    if request.method == 'GET':
        try:
            notice = Notice.objects.get(id=notice_id)
        except Notice.DoesNotExist:
            raise Http404     
        notice.is_deleted = True
        notice.save()
        
    return HttpResponseRedirect('/notice')






# add your own views here
def about(request):
    return render(request,'about.html')