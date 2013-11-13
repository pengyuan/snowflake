#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Django settings for pythonic project.
import os

#ROOT = os.path.dirname(os.path.abspath(__file__))
# path = lambda *a: os.path.join(ROOT, *a)
#  
# prev_sys_path = list(sys.path)
# site.addsitedir(path('apps'))
# new_sys_path = []
# for item in list(sys.path):
#     if item not in prev_sys_path:
#         new_sys_path.append(item)
#         sys.path.remove(item)
#          
#  
# sys.path[:0] = new_sys_path
# path = ROOT
# print path
# if path not in sys.path:
#     sys.path.append(path)
# os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
# raise Exception("DJANGO_SETTINGS_MODULE = " + str(os.environ["DJANGO_SETTINGS_MODULE"]))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

ROOT_PATH = os.path.dirname(__file__).replace('\\', '/')
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
#USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(ROOT_PATH,'media').replace('\\', '/')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(ROOT_PATH,'static').replace('\\', '/')
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH,'assets').replace('\\', '/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# SECRET_KEY用于hash，此key仅用于开发环境（生产环境请运行scripts/secret_key_gen.py）
SECRET_KEY = '_04!u)*7(p88xdwj9(7yv+m48okjf9l!v#*as8bu)x!47#z$na'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH,'templates').replace('\\', '/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',        #静态资源管理的app，在DEBUG=False的时候会自动关闭
    'django.contrib.admin',
    'django.contrib.markup',
    'apps.site',
    'apps.accounts',
    'apps.topic',
    'apps.pypi',
    'apps.people',
    'apps.pagedown',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

WMD_SHOW_PREVIEW = True
WMD_ADMIN_SHOW_PREVIEW = True

#WHOOSH_INDEX = 'c:/index'

# from django import template  
# template.add_to_builtins('topic.templatetags.template_tags')

# EMAIL_HOST = ''
# EMAIL_PORT = 25
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

try:
    from local_settings import *
except ImportError:
    pass

# 最大可上传图片大小 MB
AVATAR_UPLOAD_MAX_SIZE =  5
# 头像目录 - 需要在项目的settings.py中设置
AVATAR_DIR = os.path.join(MEDIA_ROOT,'avatar').replace('\\', '/')
# 上传的原始图片目录, 默认和头像目录相同
AVATAR_TEMP_DIR = os.path.join(MEDIA_ROOT,'temp').replace('\\', '/')
if not os.path.isdir(AVATAR_DIR):
    os.mkdir(AVATAR_DIR)
if not os.path.isdir(AVATAR_TEMP_DIR):
    os.mkdir(AVATAR_TEMP_DIR)
# 原始上传的图片url前缀，用于在裁剪选择区域显示原始图片
AVATAR_UPLOAD_URL_PREFIX = '/media/temp/'
# 剪裁后的大小 px
AVATAR_RESIZE_SIZE = 48
AVATAR_LARGE_RESIZE_SIZE = 100
# 头像处理完毕后保存的格式和质量， 格式还可以是 jpep, gif
AVATAR_SAVE_FORMAT = 'png'
AVATAR_SAVE_QUALITY = 90