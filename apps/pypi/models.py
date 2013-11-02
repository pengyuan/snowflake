#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db import models

#实现量化招聘？

class Raw(models.Model):
    name = models.CharField(max_length=30,blank=False,null=False,unique=False)
    slug = models.CharField(max_length=30)
    icon = models.CharField(max_length=50)
    category = models.CharField(max_length=30)
    label = models.CharField(max_length=30)
    description = models.TextField()
    homepage = models.URLField(max_length=50)
    license = models.CharField(max_length=20)
    github = models.URLField(max_length=30)
    language = models.CharField(max_length=20)
    os = models.CharField(max_length=20)

#软件：名称，Slug，图标，类别，截图，标签，描述，主页，协议，GitHub，开发语言，操作系统，得分，打分用户数，关注用户
class Software(models.Model):
    name = models.CharField(max_length=30,blank=False,null=False,unique=False)
    slug = models.CharField(max_length=30)
    #icon = models.ImageField()
    #category = models.ForeignKey('Category',null=True)
    #screenshot = models.ImageField()
    #label = models.ManyToManyField('Label')
    label = models.CharField(max_length=30)
    description = models.TextField()
    homepage = models.URLField(max_length=50)
    license = models.CharField(max_length=20)
    github = models.URLField(max_length=30)
    language = models.CharField(max_length=20)
    os = models.CharField(max_length=20)
    #score = models.FloatField()
    #num_score = models.IntegerField()
    #focus = models.ManyToManyField(User)
    #like = models.ManyToManyField(User)
    
    def __unicode__(self):
        return self.name

#类别：名称，Slug，是否有父类别，父类别（按xx分类）   
class Category(models.Model):
    name = models.CharField(max_length=10)
    slug = models.CharField(max_length=10)
    has_parent = models.BooleanField()
    parent = models.ForeignKey('self')
 
#评价：软件，用户，标题，内容，打分，时间 
class Comment(models.Model):
    software = models.ForeignKey(Software)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    content = models.TextField()
    score = models.IntegerField()
    time = models.DateTimeField()

#笔记：软件，用户，内容，时间，推荐
class Note(models.Model):
    software = models.ForeignKey(Software)
    user = models.ForeignKey(User)
    content = models.TextField()
    time = models.DateTimeField()
    #recommend = models.ManyToManyField(User)
# 
# #标签：软件，名称，用户，添加时间
class Label(models.Model):
    software = models.ForeignKey(Software,related_name="software_set")
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User)
    time = models.DateTimeField()
# 
# #添加/更改信息：软件，类别，描述，主页，协议，GitHub，开发语言，操作系统，提交时间，提交用户，是否审核
class Add(models.Model):
    software = models.ForeignKey(Software)
    category = models.ForeignKey(Category)
    description = models.TextField()
    homepage = models.URLField()
    license = models.CharField(max_length=20)
    github = models.URLField()
    language = models.CharField(max_length=20)
    os = models.CharField(max_length=20)
    time = models.DateTimeField()
    user = models.ForeignKey(User)
    is_checked = models.BooleanField() 

#喜欢：软件，用户，时间
class Like(models.Model):
    software = models.ForeignKey(Software)
    user = models.ForeignKey(User)
    time = models.DateTimeField()
    
#有用：评价，是否有用，用户，时间
class Help(models.Model):
    comment = models.ForeignKey(Comment)
    is_helpful = models.BooleanField()
    user = models.ForeignKey(User)
    time = models.DateTimeField()
    
#推荐：笔记，用户，时间
class Recommend(models.Model):
    note = models.ForeignKey(Note)
    user = models.ForeignKey(User)
    time = models.DateTimeField()