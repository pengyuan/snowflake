#!/usr/bin/python
# -*- coding: utf-8 -*-
from apps.accounts.pinyin import PinYin
import os
test = PinYin()
test.load_word()
print test.hanzi2pinyin(string='eric')
print test.hanzi2pinyin_split(string='eric', split="-")


print os.path.join('/root','debug.log').replace('\\', '/')