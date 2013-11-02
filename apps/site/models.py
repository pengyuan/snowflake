#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from django.db import models

#反馈：内容，创建时间，用户（匿名）
class Feedback(models.Model):
    content = models.SlugField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,null=True)

    def __unicode__(self):
        return self.name
    

# analyzer = RegexAnalyzer(ur'([\u4e00-\u9fa5])|(\w+(\.?\w+)*)')
# WHOOSH_SCHEMA = fields.Schema(title=fields.TEXT(stored=True),
#                               content=fields.TEXT(analyzer=analyzer),
#                               url=fields.ID(stored=True, unique=True))
# 
# def create_index(sender=None, **kwargs):
#     if not os.path.exists(settings.WHOOSH_INDEX):
#         os.mkdir(settings.WHOOSH_INDEX)
# #         storage = FileStorage(settings.WHOOSH_INDEX)
# #         ix = index.Index(storage, schema=WHOOSH_SCHEMA, create=True)
#         ix = create_in(settings.WHOOSH_INDEX, WHOOSH_SCHEMA)
# 
# signals.post_syncdb.connect(create_index)
# 
# def update_index(sender, instance, created, **kwargs):
# #     storage = FileStorage(settings.WHOOSH_INDEX)
# #     ix = index.Index(storage, schema=WHOOSH_SCHEMA)
#     ix = create_in(settings.WHOOSH_INDEX, WHOOSH_SCHEMA)
#     writer = ix.writer()
#     if created:
#         writer.add_document(title=unicode(instance), content=instance.content,
#                                     url=unicode(instance.get_absolute_url()))
#         writer.commit()
#     else:
#         writer.update_document(title=unicode(instance), content=instance.content,
#                                     url=unicode(instance.get_absolute_url()))
#         writer.commit()
# 
# signals.post_save.connect(update_index, sender=Topic)