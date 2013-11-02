#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.site.models import Feedback
from django import forms


class FeedbackForm(forms.ModelForm):
    content = forms.CharField(label=u'内容',widget=forms.Textarea(attrs={'class':'span12'}))
    class Meta:
        model = Feedback
        fields = ('content',)