#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
WSGI config for pythonic project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
from django.core.wsgi import get_wsgi_application
import os
import sys

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "pythonic.settings"
p1 = os.path.abspath(os.path.dirname(__file__))
p2 = os.path.abspath(os.path.join(p1,'apps'))
sys.path.append(p1)
sys.path.append(p2)
#sys.path.append('D:/Python/Python26/Lib/site-packages/django') 
#sys.path.append(ROOT_PATH)

#重定向输出，如果有错误信息打印，或者调用print打印信息，将输出到apache的error.log日志文件中。
sys.stdout = sys.stderr

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
