#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.accounts.models import User
from django import forms
from django.http.response import HttpResponseRedirect
from settings import EMAIL_ACTIVE
             
class RegisterForm(forms.Form):
    username = forms.EmailField(label=u'邮箱',required=True,max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'邮箱','autocomplete':'off'}))
    password = forms.CharField(label=u'密码',required=True,max_length=20,min_length=6,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'密码','autocomplete':'off'}))   
    name = forms.CharField(label=u'名号',required=True,max_length=20,min_length=2,help_text=u"请使用半角的 a-z 或数字 0-9",widget=forms.TextInput(attrs={'class':'form-control col-md-1','placeholder':'名号','autocomplete':'off'}))

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            if user.is_active:
                pass
            else:
                if EMAIL_ACTIVE:
                    return HttpResponseRedirect('/accounts/active/%s/not_active' % user.get_profile().slug)
            raise forms.ValidationError(u"邮箱已被注册")
        return username
        
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        try:
            User.objects.get(name=name)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(u"此名号已被占用")
        return name
   
    
class LoginForm(forms.Form):
    email = forms.EmailField(label=u'邮箱',required=True,max_length=30,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'邮箱','autocomplete':'off'}))
    password = forms.CharField(label=u'密码',required=True,max_length=20,min_length=6,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'密码','autocomplete':'off'}))
    
    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        try:
            User.objects.get(username=email)
        except User.DoesNotExist:
            raise forms.ValidationError(u"该邮箱未注册")
        else:
            return email

    
class ProfileForm(forms.ModelForm):
    username = forms.EmailField(label=u'邮箱',required=True,max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'邮箱','autocomplete':'off'}))
    name = forms.CharField(label=u'名号',required=True,max_length=20,min_length=2,help_text=u"请使用半角的 a-z 或数字 0-9",widget=forms.TextInput(attrs={'class':'form-control col-md-1','placeholder':'名号','autocomplete':'off'}))
    website = forms.CharField(label=u'博客',max_length=30,required=False,widget=forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}))
    city = forms.CharField(label=u'城市',required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    signature = forms.CharField(label=u'签名',max_length=40,required=False,widget=forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        user = kwargs.pop('instance',None)
        self.new_name = user.name
           
    #自定义规则早于表单自带规则
    def clean_name(self):
        cleaned_data = super(ProfileForm, self).clean()
        name = cleaned_data.get("name")
        try:
            user = User.objects.get(name=name)
        except (User.DoesNotExist,ValueError):
            return name
        else:
            if user.name == self.new_name:
                return name
            else:
                raise forms.ValidationError(u"此名号已被占用")
        
    class Meta:
        model = User
        fields = ('username','name','website','city','signature')