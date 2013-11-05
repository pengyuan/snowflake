# import os
# import sys
# from datetime import datetime
# 
# from fabric.api import *
# from fabric.colors import *
# 
# 
# def set_env():
#     env.FABFILE_NAME = 'production'
#     env.PROJECT_NAME = 'jojogo'
#     env.PROJECT_PATH_REMOTE = '/src/jojogo'
#     env.PROJECT_PATH_LOCAL = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
#     env.SOURCE_VIRTUALENVWRAPPER = 'source /usr/local/bin/virtualenvwrapper.sh'
#     env.VIRTUALENV_NAME = env.PROJECT_NAME
#     env.VIRTUALENV_WORKON = '%s && workon %s' % (env.SOURCE_VIRTUALENVWRAPPER, env.VIRTUALENV_NAME)
# 
#     env.host_string = 'REMOTE SERVER IP'
#     env.user = 'REMOTE SERVER SSH LOGIN USERNAME'
#     env.key_filename = 'ABSOLUTE PATH OF KEY PAIR FILE'
# 
# 
# 
# @task
# def checkout():
#     '''
#     Checkout project from Subversion
#     '''
# 
#     set_env()
# 
#     sudo('apt-get update')
#     sudo('apt-get install git mercurial subversion')
#     run('svn co --username USERNAME https://SVN_REPO_URL/')
# 
# 
# @task
# def setup():
#     '''
#     Install all services & apps
#     '''
# 
#     def install_postgresql_and_postgis():
#         sudo('apt-get install binutils gdal-bin libproj-dev postgresql-9.1-postgis postgresql-server-dev-9.1 python-psycopg2')
# 
#     def install_nginx():
#         run('wget http://nginx.org/keys/nginx_signing.key')
#         sudo('apt-key add nginx_signing.key')
#         put('config/etc/apt/sources.list.d/nginx.list', '/etc/apt/sources.list.d/nginx.list', use_sudo=True)
#         sudo('apt-get update')
#         sudo('apt-get install nginx')
# 
#         # 上傳配置文件
#         put('config/nginx/nginx.conf', '/etc/nginx.conf', use_sudo=True)
#         put('config/nginx/conf.d/guangdj.conf', '/etc/nginx/conf.d/guangdj.conf', use_sudo=True)
# 
#         # 刪除範例的配置文件
#         sudo('rm /etc/nginx/conf.d/default.conf')
#         sudo('rm /etc/nginx/conf.d/example_ssl.conf')
# 
#         sudo('service nginx restart')
# 
#     def install_pip():
#         sudo('curl http://python-distribute.org/distribute_setup.py | python')
#         sudo('curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python')
# 
#     def install_virtualenvwrapper():
#         sudo('pip install virtualenvwrapper')
# 
#     def install_pil():
#         sudo('apt-get install apt-get build-dep python-imaging')
# 
#     def install_uwsgi():
#         sudo('apt-get install build-essential python-dev libxml2-dev')
# 
#         log_dir = '~/log/uwsgi'
# 
#         run('mkdir -p %s' % log_dir)
#         run('touch %s/guangdj.log' % log_dir)
# 
#     set_env()
# 
#     install_postgresql_and_postgis()
#     install_nginx()
#     install_pip()
#     install_virtualenvwrapper()
#     install_pil()
#     install_uwsgi()
# 
#     with prefix(env.SOURCE_VIRTUALENVWRAPPER):
#         '''
#         必須 source virtualenvwrapper.sh
#         否則會出現 /bin/sh: workon: command not found
#         '''
# 
#         run('mkvirtualenv --no-site-packages %s' % env.VIRTUALENV_NAME)
# 
#         with prefix(env.VIRTUALENV_WORKON):
#             with cd(env.PROJECT_PATH_REMOTE):
#                 run('pip install -r requirements.txt')
#                 run('yolk -l')
#                 run('mkdir -p static_root')
#                 run('python manage.py collectstatic --clear --noinput')
# 
# 
# @task
# def syncdb():
#     '''
#     Update & migrate Django database
#     '''
# 
#     set_env()
# 
#     with prefix(env.VIRTUALENV_WORKON):
#         run('python manage.py syncdb')
# 
# 
# @task
# def nginx():
#     '''
#     Reload nginx
#     '''
# 
#     set_env()
# 
#     sudo('service nginx restart')
# 
# 
# @task
# def celery():
#     '''
#     Reload Celery
#     '''
# 
#     set_env()
# 
#     with prefix(env.VIRTUALENV_WORKON):
#         try:
#             sudo("ps auxww | grep 'celery' | awk '{print $2}' | xargs kill -9")
#         except:
#             print(green('雖然有錯誤訊息，但是 celeryd 還是有被 kill'))
# 
#         sudo('python manage.py celeryd_detach')
# 
# 
# @task
# def uwsgi():
#     '''
#     Reload uWSGI
#     '''
# 
#     set_env()
# 
#     with prefix(env.VIRTUALENV_WORKON):
#         run('svn up')
#         run('python manage.py collectstatic --clear --noinput')
#         run('killall -9 uwsgi')
#         run('uwsgi --ini config/uwsgi_conf.ini')