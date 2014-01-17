#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.accounts.forms import RegisterForm, LoginForm, ProfileForm
from apps.accounts.models import User
from apps.accounts.utils import send_email
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from settings import EMAIL_ACTIVE, SITE_NAME, DOMAIN
import hashlib
import time

@csrf_protect
def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request,'register.html',{'form':form})
    form = RegisterForm(request.POST)
    if form.is_valid():
        data = form.clean()
        new_user = User.objects.create_user(username=data['username'],password=data['password'],name=data['name'])
        if EMAIL_ACTIVE:
            new_user.is_active = False
        else:
            new_user.is_active = True
        new_user.save()
        return HttpResponseRedirect('/accounts/active/%s/not_active' % new_user.name)           
    else:
        return render(request,'register.html',{"form":form})

@csrf_protect
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    if request.method == 'GET':
        referer  = request.META.get('HTTP_REFERER','/')
        if 'accounts' in str(referer) or 'notice' in str(referer) or 'admin' in str(referer):
            request.session['referer'] = '/'
        else :
            request.session['referer'] = referer
        form = LoginForm()
        return render(request,'login.html',locals())
    form = LoginForm(request.POST)
    if form.is_valid():
        data = form.clean()
        user = User.objects.get(username=data['email'])
        user = authenticate(username=data['email'],password=data['password'])
        #print data['password']
        #print user.check_password(data['password'])
        #if user.check_password(data['password']):
#         print user
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                nextpage = request.session.get('referer','/') # 下页地址
                is_auto_login = request.POST.get('auto')
                if not is_auto_login:
                    request.session.set_expiry(0)
                return HttpResponseRedirect(nextpage)
            else:
                return HttpResponseRedirect('/accounts/active/%s/not_active' % user.get_profile().slug)
        else:
            messages.error(request,'密码不正确！')
            return render(request,'login.html',locals())
    else:
        return render(request,'login.html',{"form":form})        
 
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/accounts/login')

def active(request,u_name,active_code):
    try:
        user = User.objects.get(name=u_name)
    except (User.DoesNotExist,ValueError):
        return HttpResponseRedirect('/')
    if user.is_active:
        messages.success(request,'账号已经激活，请直接登录')
        return HttpResponseRedirect('/accounts/login')
    # 验证激活码是否正确   
    elif active_code == _get_active_code(user.username):
        user.is_active = True
        user.save()
        messages.success(request,'恭喜，账号激活成功！请登录')
        return HttpResponseRedirect('/accounts/login')
    elif active_code == 'not_active':
        active_url = '%s/accounts/active/%s/%s' %('http://'+DOMAIN,user.get_profile().slug,_get_active_code(user.username))
        subject = SITE_NAME+'-账号激活邮件'
        body = loader.render_to_string('registration/active_email.html',{'user':user,'active_url':active_url})
        from_email = '"'+SITE_NAME+'" <no-reply@'+DOMAIN+'>'
        to = [user.username]
        # 开启发送激活邮件线程
        send_email(subject,body,from_email,to)
        #  根据邮件地址找到信箱登录地址
        email_domains = {
            'qq.com':'mail.qq.com',
            'foxmail.com':'mail.qq.com',
            'gmail.com':'www.gmail.com',
            '126.com':'www.126.com',
            '163.com':'www.163.com',
            '189.cn':'www.189.cn',
            '263.net':'www.263.net',
            'yeah.net':'www.yeah.net',
            'sohu.com':'mail.sohu.com',
            'tom.com':'mail.tom.com',
            'hotmail.com':'www.hotmail.com',
            'yahoo.com.cn':'mail.cn.yahoo.com',
            'yahoo.cn':'mail.cn.yahoo.com',
            '21cn.com':'mail.21cn.com',
        }
        for key,value in email_domains.items():
            if user.username.count(key) >= 1:
                email_domain = value
                break
        return render(request,'registration/active.html',locals())
    else:
        raise Http404()
 
def _get_active_code(email):
    date_str = time.strftime('%Y-%m-%d',time.localtime()) # 当天内有效
    m = hashlib.md5(str(email)+'snowflake'+'axweraf9092443lklnfd0f89d1988'+date_str)
    return m.hexdigest()

@login_required
def settings(request):
    user = request.user
    if request.method == 'GET':
        form = ProfileForm(instance=user)
        return render(request,'settings.html',locals())
    form = ProfileForm(request.POST,instance=user)
    if form.is_valid():
        form.save(commit=True)
        messages.success(request,"设置已更新")
        return render(request,'settings.html',{"form":form})
    else:
        return render(request,'settings.html',{"form":form})
    
@login_required
def password_change(request):
    if request.method == 'GET':
        form = PasswordChangeForm()
        return render(request,'password_change.html',locals())
    form = PasswordChangeForm(request.POST)
    if form.is_valid():
        data = form.clean()
        user = request.user
        if user.check_password(data['oldpassword']):
            user.password = data['newpassword']
            user.save()
            messages.success(request,"新密码设置成功！请重新登录")
            return HttpResponseRedirect('/accounts/logout')
        else:
            messages.error(request,'当前密码输入错误')
            return render(request,'password_change.html',{"form":form})
    else:
        return render(request,'password_change.html',{"form":form})    