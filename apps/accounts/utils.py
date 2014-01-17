#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.core.mail import EmailMessage
import threading
import time

class EmailThread(threading.Thread):
    """
    发送账号激活邮件线程
    """
    def __init__(self,subject='', body='', from_email=None, to=None):
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.to = to
        self.fail_silently = True
        threading.Thread.__init__(self)

    def run(self):
        msg_email = EmailMessage(self.subject,self.body,self.from_email,self.to)
        msg_email.content_subtype = 'html'
        try:
            msg_email.send(self.fail_silently)
        except Exception,e:
            # 记录错误日志
            log = open('email_error.log','a')
            log.write('%s %s\n' %(time.strftime('%Y-%m-%d %H:%M:%S'),e) )
            log.close()

def send_email(subject='', body='', from_email=None, to=[]):
    """
    发送邮件方法
    """
    email = EmailThread(subject, body, from_email, to)
    email.start()
    email.join()