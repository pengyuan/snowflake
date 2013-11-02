#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.accounts.models import UserProfile
from django.contrib import admin

admin.site.register(UserProfile)