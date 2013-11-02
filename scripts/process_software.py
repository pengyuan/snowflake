#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from apps.pypi.models import Raw
import urlparse

#目标：
#1.icon下载下来，重命名
#2.category分类
#3.label中文分词，tag外键化
#4.description转换
#5.language，license，os外键化（license未知转为None）

raw_list = Raw.objects.all()
for item in raw_list:
    link = urlparse.urljoin('http://www.oschina.net',item.icon)