#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from PIL import Image
from apps.accounts.forms import RegisterForm, LoginForm, ProfileForm
from apps.accounts.function import send_email
from apps.accounts.models import UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, \
    logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import loader
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_protect
from functools import wraps
from settings import AVATAR_UPLOAD_MAX_SIZE, AVATAR_TEMP_DIR, \
    AVATAR_UPLOAD_URL_PREFIX, AVATAR_RESIZE_SIZE, AVATAR_SAVE_FORMAT, AVATAR_DIR, \
    AVATAR_SAVE_QUALITY, AVATAR_LARGE_RESIZE_SIZE, DOMAIN
from urllib import urlretrieve
import hashlib
import os
import time
import urllib2

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request,'register.html',{'form':form})
    form = RegisterForm(request.POST)
    zen = request.POST.get('zen')
    if not zen:
        messages.error(request,'请仔细阅读《Pythonic社区指导原则》')
        return render(request,'register.html',{"form":form,"zen":zen})
    if form.is_valid():
        data = form.clean()
    else:
        return render(request,'register.html',{"form":form,"zen":zen})
    try:
        user = User.objects.get(username=data['email'])
    except User.DoesNotExist:
        pass
    else:
        if user.is_active:
            messages.error(request,'该邮箱已被注册，请更换邮箱')
            return render(request,'register.html',{"form":form,"zen":zen})
        else:
            return HttpResponseRedirect('/accounts/active/%s/not_active' % user.get_profile().slug)
    try:
        user = UserProfile.objects.get(name=data['name'])
    except UserProfile.DoesNotExist:
        pass
    else:
        messages.error(request,'此名号已被占用')
        return render(request,'register.html',{"form":form,"zen":zen})
    try:
        user = UserProfile.objects.get(slug=data['slug'])
    except UserProfile.DoesNotExist:
        pass
    else:
        messages.error(request,'此个性网址已存在')
        return render(request,'register.html',{"form":form,"zen":zen})
    # 创建新用户      
    new_user = User.objects.create_user(username=data['email'],email=data['email'],password=data['password'])
    new_user.is_active = False
     
    avatar_name = hashlib.md5(data['email'].lower()).hexdigest()
    gravatar_url = ''.join(['http://www.gravatar.com/avatar/',avatar_name, '?s=48&d=404'])
    res_name = '%s-normal.%s' % (avatar_name, AVATAR_SAVE_FORMAT)
    res_path = os.path.join(AVATAR_DIR, res_name)
    req = urllib2.Request(gravatar_url)
    try:
        urllib2.urlopen(req)      
    except urllib2.HTTPError, e:
        new_profile = UserProfile(user=new_user,name=data['name'],slug=data['slug'].lower(),province=data['province'],city=data['city'])
        pass
    else:
        urlretrieve(gravatar_url,res_path)
        gravatar_url = ''.join(['http://www.gravatar.com/avatar/',avatar_name, '?s=100&d=404'])
        res_name2 = '%s-large.%s' % (avatar_name, AVATAR_SAVE_FORMAT)
        res_path = os.path.join(AVATAR_DIR, res_name2)
        urlretrieve(gravatar_url,res_path)
        new_profile = UserProfile(user=new_user,name=data['name'],slug=data['slug'].lower(),province=data['province'],city=data['city'],avatar=res_name,photo=res_name2)
    try:
        new_user.save()
        new_profile.save()
        return HttpResponseRedirect('/accounts/active/%s/not_active' % new_user.get_profile().slug)
    except Exception,e:
        messages.error(request,'服务器出现错误：%s' %e)
    return render(request,'register.html',{"form":form,"zen":zen})

@csrf_protect
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    if request.method == 'GET':
        referer  = request.META.get('HTTP_REFERER','/')
        print referer
        if 'accounts' in str(referer) or 'notice' in str(referer) or 'message' in str(referer) or 'admin' in str(referer):
            request.session['referer'] = '/'
        else :
            request.session['referer'] = referer
        print request.session['referer']
        form = LoginForm()
        return render(request,'login.html',locals())
    form = LoginForm(request.POST)
    if form.is_valid():
        data = form.clean()
        # 检查email是否存在
        try:
            user = User.objects.get(username=data['email'])
        except User.DoesNotExist:
            messages.error(request,"该邮箱未注册")
            return render(request,'login.html',locals())
        user = authenticate(username=data['email'],password=data['password'])
        if user is not None:
            if user.is_active:
                auth_login(request,user)
                nextpage = request.session.get('referer','/') # 下页地址
                is_auto_login = request.POST.get('auto')
                if not is_auto_login:
                    request.session.set_expiry(0)
                return HttpResponseRedirect(nextpage)
            else:
                return HttpResponseRedirect('/accounts/active/%s/not_active' % user.get_profile().slug)
        else:
            messages.error(request,'密码错误！')
    return render(request,'login.html',locals())
 
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/accounts/login')

def active(request,u_slug,active_code):
    try:
        user_profile = UserProfile.objects.get(slug=u_slug)
    except (UserProfile.DoesNotExist,ValueError):
        return HttpResponseRedirect('/')
    user = user_profile.user
    # 已经激活过
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
        subject = 'Pythonic-账号激活邮件'
        body = loader.render_to_string('registration/active_email.html',{'user':user,'active_url':active_url})
        from_email = '"Pythonic社区" <no-reply@pythonic.org>'
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
    m = hashlib.md5(str(email)+'pythonic'+'axweraf9092443lklnfd0f89d1988'+date_str)
    return m.hexdigest()

@login_required
def accounts(request):
    profile = request.user.get_profile()
    if request.method == 'GET':
        form = ProfileForm(instance=profile)
        return render(request,'accounts.html',locals())
    form = ProfileForm(request.POST,instance=profile)
    if form.is_valid():
        form.save()
        messages.success(request,"个人资料更新成功")
        return render(request,'accounts.html',{"form":form})
    else:
        return render(request,'accounts.html',{"form":form})    

@login_required
def change_avatar(request):
    return render(request,'avatar.html')

border_size = 300

test_func = lambda request: request.method == 'POST' and request.user


class UploadAvatarError(Exception):
    pass


def protected(func):
    @wraps(func)
    def deco(request, *args, **kwargs):
        if not test_func(request):
            return HttpResponse(
                "<script>window.parent.upload_avatar_error('%s')</script>" % '禁止操作'
            )
        try:
            return func(request, *args, **kwargs)
        except UploadAvatarError as e:
            return HttpResponse(
                "<script>window.parent.upload_avatar_error('%s')</script>" % e
            )
    return deco


@protected
@login_required
def upload_avatar(request):
    try:
        uploaded_file = request.FILES['uploadavatarfile']
    except KeyError:
        raise UploadAvatarError('请正确上传图片')

    if uploaded_file.size > AVATAR_UPLOAD_MAX_SIZE * 1024 * 1024:
        raise UploadAvatarError('图片不能大于{0}MB'.format(AVATAR_UPLOAD_MAX_SIZE))

    ext = os.path.splitext(uploaded_file.name)[-1]
    new_name = hashlib.md5('{0}{1}'.format(get_random_string(), time.time())).hexdigest()
    new_name = '%s%s' % (new_name, ext.lower())
    fpath = os.path.join(AVATAR_TEMP_DIR, new_name)
    try:
        with open(fpath, 'wb') as f:
            for c in uploaded_file.chunks(10240):
                f.write(c)
    except IOError:
        raise UploadAvatarError('发生错误，稍后再试')
    try:
        Image.open(fpath)
    except IOError:
        try:
            os.unlink(fpath)
        except:
            pass
        raise UploadAvatarError('请正确上传图片')
    request.session['photo_name'] = new_name

    return HttpResponse(
        "<script>window.parent.upload_avatar_success('%s')</script>" % (
            AVATAR_UPLOAD_URL_PREFIX + new_name
        )
    )

@protected
@login_required
def crop_avatar(request):
    """剪裁头像"""
    photo_name = request.session['photo_name']
    photo_orig = os.path.join(AVATAR_TEMP_DIR, photo_name)
    try:
        x1 = int(float(request.POST['x1']))
        y1 = int(float(request.POST['y1']))
        x2 = int(float(request.POST['x2']))
        y2 = int(float(request.POST['y2']))
    except:
        raise UploadAvatarError('发生错误，稍后再试')

    try:
        orig = Image.open(photo_orig)
    except IOError:
        raise UploadAvatarError('发生错误，请重新上传图片')

    orig_w, orig_h = orig.size
    if orig_w <= border_size and orig_h <= border_size:
        ratio = 1
    else:
        if orig_w > orig_h:
            ratio = float(orig_w) / border_size
        else:
            ratio = float(orig_h) / border_size

    box = [int(x * ratio) for x in [x1, y1, x2, y2]]
    avatar = orig.crop(box)
    avatar_name, _ = os.path.splitext(photo_name)
        
    size = AVATAR_RESIZE_SIZE
    size_large = AVATAR_LARGE_RESIZE_SIZE
    try:
        res = avatar.resize((size, size), Image.ANTIALIAS)
        res2 = avatar.resize((size_large, size_large), Image.ANTIALIAS)
        res_name = '%s-normal.%s' % (avatar_name, AVATAR_SAVE_FORMAT)
        res_name2 = '%s-large.%s' % (avatar_name, AVATAR_SAVE_FORMAT)
        res_path = os.path.join(AVATAR_DIR, res_name)
        res_path2 = os.path.join(AVATAR_DIR, res_name2)
        res.save(res_path, AVATAR_SAVE_FORMAT, quality=AVATAR_SAVE_QUALITY)
        res2.save(res_path2, AVATAR_SAVE_FORMAT, quality=AVATAR_SAVE_QUALITY)
    except:
        raise UploadAvatarError('发生错误，请稍后重试')
    
    for files in os.walk(AVATAR_TEMP_DIR):
        for fn in files[2]:
            filePath = os.path.join(AVATAR_TEMP_DIR,fn)
            if os.path.isfile( filePath ):
                try:
                    os.unlink(photo_orig)
                except OSError:
                    pass
 
    if UserProfile.objects.filter(user=request.user).exists():
        _obj = UserProfile.objects.get(user=request.user)
        _obj.delete_photo()
        _obj.delete_avatar()
        _obj.photo = res_name2
        _obj.avatar = res_name
        _obj.save()

    messages.info(request,'已更新')
    return HttpResponse(
        "<script>window.parent.crop_avatar_success('%s')</script>"  % '成功'
    )