#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.site.forms import FeedbackForm
from apps.topic.models import Topic, Node, ParentNode
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
import datetime
#from main.models import WHOOSH_SCHEMA

def index(request):
    context = {}
#     context['topics'] = Topic.objects.all().order_by('-updated_on')[:10]
#     context['nodes'] = Node.objects.all()[:10]

    topic_list = Topic.objects.all().order_by('-updated_on')
    paginator = Paginator(topic_list, 20) # Show 20 contacts per page

    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        topics = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        topics = paginator.page(paginator.num_pages)
    context['topics'] = topics
    
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
    from_date = time_now - datetime.timedelta(days=7)
    hot_topics = Topic.objects.filter(created_on__range=[from_date, time_now]).order_by('num_replies')[:10]
    context['hot_topics'] = hot_topics
    hot_nodes = Node.objects.filter(num_topics__gt=0,updated_on__gt=from_date).order_by('updated_on')[:10]
    context['hot_nodes'] = hot_nodes
    return render(request,'index.html',context)

#def search(request):
#     context = {}
# #     p = Topic(title='first post', body='This is my first post')
# #     p.save() # The new model is already added to the index
#     if request.method =='GET':
#         get = request.GET.copy()
#         if get.has_key('q'):
#             query = get['q']
#             hits = Topic.objects.query(query)
#             
#             context['query'] = query
#             context['hits'] = hits
#     return render(request,'search.html',context)
# 
# """
#     Simple search view, which accepts search queries via url, like google.
#     Use something like ?q=this+is+the+serch+term
# 
#     """
#    context = {}
#     storage = FileStorage(settings.WHOOSH_INDEX)
#     ix = index.Index(storage, schema=WHOOSH_SCHEMA)
#     ix = create_in(settings.WHOOSH_INDEX, WHOOSH_SCHEMA)
#     hits = []
#     query = request.GET.get('q', None)
#     if query is not None and query != u"":
#         # Whoosh don't understands '+' or '-' but we can replace
#         # them with 'AND' and 'NOT'.
#         #query = query.replace('+', ' AND ').replace(' -', ' NOT ')
#         context['query'] = query
#         parser = QueryParser("content", schema=ix.schema)
#         try:
#             qry = parser.parse(query)
#         except:
#             # don't show the user weird errors only because we don't
#             # understand the query.
#             # parser.parse("") would return None
#             qry = None
#         if qry is not None:
# #             searcher = ix.searcher()
# #             hits = searcher.search(qry)
#             with ix.searcher() as searcher:
#                 hits = searcher.find('content', u'哈')
#                  
#                 #hits = searcher.search(qry)
#                 context['hits'] = hits
#             
#     return render(request,'search.html',context)

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