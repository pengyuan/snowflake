#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.http.response import Http404
from django.shortcuts import render
from apps.pypi.models import Raw

def pypi(request):
    context = {}
    #software_list = Software.objects.filter(language='Python')[:10]
    software_list = Raw.objects.all()[:10]
    language_list = Raw.objects.values_list('language').distinct()
    context['software_list'] = software_list
    context['language_list'] = language_list
#     node = Node.objects.get(id=node_id)
# #    try:
# #        node = Node.objects.get(id=node_id)
# #    except Node.DoesNotExist:
# #        raise Http404
#     context['node'] = node
#     context['topic_list'] = Topic.objects.filter(node=node).order_by('-updated_on')
#     if request.user.is_authenticated():
#         user_list = node.users.all()
#         node_list = request.user.node_set.all()
#         if node in node_list:
#             context['focus'] = True
#         else:
#             context['focus'] = False
# #         nodeuser = NodeUser.objects.filter(node=node,user=request.user)
# #         if nodeuser:
# #             context['focus'] = True
# #         else:
# #             context['focus'] = False
# #         user_list = NodeUser.objects.filter(node=node).values('user')
#         context['user_list'] = user_list
#         
#     context['form'] = TopicForm()
    return render(request,'software.html',context)

def subject(request, software_id):
    context = {}
    try:
        software = Raw.objects.get(id=software_id)
    except Raw.DoesNotExist:
        raise Http404
    context['software'] = software
#     node = Node.objects.get(id=node_id)
# #    try:
# #        node = Node.objects.get(id=node_id)
# #    except Node.DoesNotExist:
# #        raise Http404
#     context['node'] = node
#     context['topic_list'] = Topic.objects.filter(node=node).order_by('-updated_on')
#     if request.user.is_authenticated():
#         user_list = node.users.all()
#         node_list = request.user.node_set.all()
#         if node in node_list:
#             context['focus'] = True
#         else:
#             context['focus'] = False
# #         nodeuser = NodeUser.objects.filter(node=node,user=request.user)
# #         if nodeuser:
# #             context['focus'] = True
# #         else:
# #             context['focus'] = False
# #         user_list = NodeUser.objects.filter(node=node).values('user')
#         context['user_list'] = user_list
#         
#     context['form'] = TopicForm()
    return render(request,'subject.html',context)