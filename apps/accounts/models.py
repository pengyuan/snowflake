#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from settings import AVATAR_DIR
import os
 
#用户资料：用户，Pythonic域名，个人网站，微博，github，大头像，小头像，城市，签名，个人简介，是否注销
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=20,null=False)
    slug = models.CharField(max_length=20,null=False)
    website = models.CharField(max_length=30,blank=True)
    weibo = models.CharField(max_length=50,blank=True)
    github = models.CharField(max_length=50,blank=True)
    photo = models.CharField(max_length=50,default='default-large.png')
    avatar = models.CharField(max_length=50,default='default-normal.png')
    province = models.CharField(max_length=10,null=False)
    city = models.CharField(max_length=10,blank=True,null=True)
    signature = models.CharField(max_length=40,blank=True)
    introduction = models.CharField(max_length=200,blank=True)
    deleted = models.BooleanField(default=False)
    #follow = models.ManyToManyField(self)
    
    def __unicode__(self):
        return self.name
    
    def get_photo_path(self):
        path = os.path.join(AVATAR_DIR, self.photo)
        if not os.path.exists(path):
            return None
        return path

    def get_avatar_path(self):
        path = os.path.join(AVATAR_DIR, self.avatar)
        if not os.path.exists(path):
            return None
        return path
   
    def delete_photo(self):
        if self.photo == 'default-large.png':
            return
        path = self.get_photo_path()
        if path:
            try:
                os.unlink(path)
            except OSError:
                pass    

    def delete_avatar(self):
        if self.avatar == 'default-normal.png':
            return
        path = self.get_avatar_path()
        if path:
            try:
                os.unlink(path)
            except OSError:
                pass

# def _delete_avatar_on_disk(sender, instance, *args, **kwargs):
#     print '_delete_avatar_on_disk!!!!!!!!!!!!!!!'
#     instance.delete_photo()
# 
# post_delete.connect(_delete_avatar_on_disk, sender=UserProfile)