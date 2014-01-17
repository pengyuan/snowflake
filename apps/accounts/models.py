#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=20,unique=True,null=False)
    website = models.CharField(max_length=30,null=True,blank=True)
    city = models.CharField(max_length=10,null=True,blank=True)
    signature = models.CharField(max_length=40,null=True,blank=True)
    
    def __unicode__(self):
        return self.name