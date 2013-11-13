#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from apps.accounts.models import UserProfile
from apps.people.models import Message
from apps.topic.models import Node, Topic, Reply, ParentNode, Description
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management import call_command
from settings import DATABASES
import MySQLdb
import datetime

conn = MySQLdb.connect(host = 'localhost', user = DATABASES['default']['USER'], passwd = DATABASES['default']['PASSWORD'])
cursor = conn.cursor()

try:
    cursor.execute('drop database pythonic')
    cursor.execute('create database if not exists pythonic default charset utf8 COLLATE utf8_general_ci')
    conn.commit()
except Exception, e:
    print e
    conn.rollback()
finally:
    cursor.close()
    conn.close()
    
try:
    call_command('syncdb', interactive=True)
except Exception, e:
    print e
    pass    

conn = MySQLdb.connect(host = 'localhost', user = DATABASES['default']['USER'], passwd = DATABASES['default']['PASSWORD'], db='pythonic')
cursor = conn.cursor()
try:
    cursor.execute("use pythonic")
    cursor.execute("ALTER table topic_topic AUTO_INCREMENT=19880929")
    conn.commit()
except Exception, e:
    print e
    conn.rollback()
finally:
    cursor.close()
    conn.close()
    
#初始化用户
new_user = User.objects.create_user(username='pengyuan@gmail.com',email='pengyuan@gmail.com',password='123456')
new_user.is_active = True
new_user.save()
new_profile = UserProfile(user=new_user,name=u'Eric',slug='eric',province="湖北",city=u'武汉')
new_profile.save()
 
second_user = User.objects.create_user(username='a@gmail.com',email='a@gmail.com',password='123456')
second_user.is_active = True
second_user.save()
second_profile = UserProfile(user=second_user,name=u'Jack',slug='jack',province="北京",city=u'东城')
second_profile.save()

third_user = User.objects.create_user(username='b@gmail.com',email='b@gmail.com',password='123456')
third_user.is_active = True
third_user.save()
third_profile = UserProfile(user=third_user,name=u'Robbin',slug='robbin',province="浙江",city=u'杭州')
third_profile.save()

fourth_user = User.objects.create_user(username='c@gmail.com',email='c@gmail.com',password='123456')
fourth_user.is_active = True
fourth_user.save()
fourth_profile = UserProfile(user=fourth_user,name=u'Jim',slug='jim',province="江西",city=u'九江')
fourth_profile.save()
 
fifth_user = User.objects.create_user(username='d@gmail.com',email='d@gmail.com',password='123456')
fifth_user.is_active = True
fifth_user.save()
fifth_profile = UserProfile(user=fifth_user,name=u'Fish',slug='fish',province="广东",city=u'广州')
fifth_profile.save()

#初始化类别
cat_python = ParentNode.objects.create(name=u'Python')
cat_explore = ParentNode.objects.create(name=u'探索')
cat_web = ParentNode.objects.create(name=u'Web开发')
cat_sci = ParentNode.objects.create(name=u'科学计算')
cat_mobile = ParentNode.objects.create(name=u'Mobile')
cat_activity = ParentNode.objects.create(name=u'活动')
#初始化节点
time = datetime.datetime.now()
new_node = Node(name='Pythonic',slug='pythonic',category=cat_python,num_topics=0,created_on=time,updated_on=time)
new_node.save()
description = Description.objects.create(content=u'Life is short，be Pythonic！分享简约的技术、方法论、设计.',author=new_user,node=new_node,active=True)
description.save()
new_node = Node(name='分享',slug='share',category=cat_python,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='奇思妙想',slug='idea',category=cat_python,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='创造',slug='creation',category=cat_python,num_topics=0,created_on=time,updated_on=time)
new_node.save()

new_node = Node(name='瞎扯谈',slug='chat',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='设计',slug='design',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='TED',slug='ted',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='开源',slug='open-source',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Ruby',slug='ruby',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='创业',slug='startup',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Kindle',slug='kindle',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='黑客与画家',slug='kk',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='RESTful',slug='restful',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Rework',slug='rework',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Mac',slug='mac',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Agile',slug='agile',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='测试',slug='testing',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Lisp',slug='lisp',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='翻墙',slug='gfw',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='招聘',slug='job',category=cat_explore,num_topics=0,created_on=time,updated_on=time)
new_node.save()

new_node = Node(name='PyPI',slug='pypi',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='MongoDB',slug='mongodb',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Redis',slug='redis',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='前端开发',slug='front-end',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Web安全',slug='web-security',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='云服务',slug='cloud',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='RabbitMQ',slug='rabbitmq',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='算法',slug='algorithm',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Memcached',slug='memcached',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Git',slug='git',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Database',slug='database',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Linux',slug='linux',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Nginx',slug='nginx',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='运维',slug='operation',category=cat_web,num_topics=0,created_on=time,updated_on=time)
new_node.save()

new_node = Node(name='机器学习',slug='ml',category=cat_sci,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='可视化',slug='visualization',category=cat_sci,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='OpenStack',slug='openstack',category=cat_sci,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='自然语言处理',slug='nlp',category=cat_sci,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='GUI',slug='gui',category=cat_sci,num_topics=0,created_on=time,updated_on=time)
new_node.save()

new_node = Node(name='iOS',slug='ios',category=cat_mobile,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='Android',slug='android',category=cat_mobile,num_topics=0,created_on=time,updated_on=time)
new_node.save()
new_node = Node(name='HTML5',slug='html5',category=cat_mobile,num_topics=0,created_on=time,updated_on=time)
new_node.save()

new_node = Node(name='线下活动',slug='activity',category=cat_activity,num_topics=0,created_on=time,updated_on=time)
new_node.save()



#初始化话题1
node = Node.objects.filter(name='Pythonic')[0]
node.num_topics += 1
node.save()
new_topic = Topic(title=u'Pythonic社区上线',content=u'Pythonic是一个Python界广为人知却不知甚解的词汇。less is more / simple is better / 大道至简。这是一套实践原则，也是一种生活方式。社区为谁而建？',node=node)
new_topic.author = new_user
new_topic.last_reply = new_user
new_topic.num_views = 0
new_topic.num_replies = 0
new_topic.updated_on = datetime.datetime.now()
new_topic.save()
#初始化话题2
node = Node.objects.filter(name='招聘')[0]
node.num_topics += 1
node.save()
new_topic = Topic(title=u'Linux Deepin新增华中科技大学镜像服务(联创)',content=u'Linux Deepin在10月14日新增了华中科技大学的镜像服务。现在，我们又获得了由华中科技大学联创团队维护的另一镜像服务。该镜像站点由华中科技大学启明学院和联创团队提供，并由华中科技大学网络与计算中心提供网络支持，包括了Linux Deepin在内的多个开源软件镜像服务。在此，对他们提供的支持和帮助表示感谢。',node=node)
new_topic.author = second_user
new_topic.last_reply = second_user
new_topic.num_views = 0
new_topic.num_replies = 0
new_topic.updated_on = datetime.datetime.now()
new_topic.save()
#初始化话题3
node = Node.objects.filter(name='机器学习')[0]
node.num_topics += 1
node.save()
new_topic = Topic(title=u'数据实时性要求较高的项目该如何利用缓存?',content=u'如题,  例如OA, 银行, 电力方面的项目.  如何使用缓存呢?  有效时间设置短一些? 目前我将一些公用的以及不经常改变的东西放到缓存中了, 一些实时性要求较高的东西没有用缓存, 但是又解决的经常查数据库很不爽. SQL语句很大(暂时不说优化SQL语句的事情).还请有经验的朋友分享一下. 感谢!',node=node)
new_topic.author = third_user
new_topic.last_reply = third_user
new_topic.num_views = 0
new_topic.num_replies = 0
new_topic.updated_on = datetime.datetime.now()
new_topic.save()
#初始化话题4
node = Node.objects.filter(name='Pythonic')[0]
node.num_topics += 1
node.save()
new_topic = Topic(title=u'el表达式${ form​.userName} form为actionForm区别',content=u'struts1框架中   在页面中有${param.userName}  和 ${ form.userName}  form为actionForm类型的对象他们有区别么 可不可以使用其中的一个代替另一个  在线等希望有个高手为我解答  谢谢 ',node=node)
new_topic.author = new_user
new_topic.last_reply = new_user
new_topic.num_views = 0
new_topic.num_replies = 0
new_topic.updated_on = datetime.datetime.now()
new_topic.save()
#初始化话题5
node = Node.objects.filter(name='设计')[0]
node.num_topics += 1
node.save()
new_topic = Topic(title=u'持续交付和持续部署的区别',content=u'我在上周三写的这条微博。它在微博上激起了活跃的讨论，周四的时候已经被转发了87次，获得了25个赞。',node=node)
new_topic.author = third_user
new_topic.last_reply = third_user
new_topic.num_views = 0
new_topic.num_replies = 0
new_topic.updated_on = datetime.datetime.now()
new_topic.save()
#初始化话题6
node = Node.objects.filter(name='瞎扯谈')[0]
node.num_topics += 1
node.save()
new_topic = Topic(title=u'第三季度近半数移动钓鱼网站针对网络银行',content=u'网络银行是因为移动技术而变得更加方便的众多服务之一。如今，用户可以随时随地的购买产品、服务、支付账单和管理自己的财务。不过，现实中也存在着会攻击移动银行的威胁，必须加以解决和防护。这些威胁包括：移动钓鱼 – 恶意移动网站会伪装成正常的登入网页，像是银行或社群网络。这些网页是设计来诱骗用户输入他们的登入数据。到目前为止，这一季里有近一半的移动钓鱼网站是针对金融服务网站。',node=node)
new_topic.author = second_user
new_topic.last_reply = second_user
new_topic.num_views = 0
new_topic.num_replies = 0
new_topic.updated_on = datetime.datetime.now()
new_topic.save()
#初始化话题7
node = Node.objects.filter(name='Pythonic')[0]
node.num_topics += 1
node.save()
new_topic = Topic(title=u'XWiki 5.3 M1 发布，Java 的 Wiki 系统',content=u'XWiki 5.3 M1 是一个面向开发者的发行版本，提供新的扩展管理 API，一个 XWiki 企业 Maven 原型；改进了 XAR 插件；修复了很多 bug 等等。XWiki是一个由Java编写的基于LGPL协议发布的开源wiki和应用平台。它的开发平台特性允许创建协作式Web应用，同时也提供了构建于平台之上的打包应用（第二代wiki）。',node=node)
new_topic.author = new_user
new_topic.last_reply = new_user
new_topic.num_views = 0
new_topic.num_replies = 0
new_topic.updated_on = datetime.datetime.now()
new_topic.save()
#初始化话题8
node = Node.objects.filter(name='创造')[0]
node.num_topics += 1
node.save()
new_topic = Topic(title=u'埃洛普: 我们或许高估了 Windows Phone',content=u'埃洛普在与印度网站The Hindu的访谈中承认诺基亚自从转型至Windows Phone平台之后便遭遇到了利润上的枯竭.埃洛普如此说道:" 当你从头开始做某项任务时,过度投资总是必须的.然而若我们回过头来看,会发现Windows Phone设备的销量是呈上升趋势的.这也是微软为此感到激动的原因,因为它的轨迹朝着正确的方向发展.作为诺基亚,我们也对此进行了研究,得出了我们投 资的数量以及可以承受的过度投资,这些都是清醒的."而对于将他所执掌的部门卖给微软的决策,埃洛普表示这是为了股东的利益而考虑的.此举 将能刺激诺基亚的股价,这方面的利益要比整个交易所获得的还要多.与此同时埃洛普表示诺基亚的Lumia以及Asha品牌是否将出现在未来诺基亚设备是属 于微软的决定,因为在收购案中诺基亚已经将这些商标卖给了对方.',node=node)
new_topic.author = third_user
new_topic.last_reply = third_user
new_topic.num_views = 0
new_topic.num_replies = 0
new_topic.updated_on = datetime.datetime.now()
new_topic.save()
#初始化话题9
node = Node.objects.filter(name='分享')[0]
node.num_topics += 1
node.save()
new_topic = Topic(title=u'分享一个笑话',content=u'一个疯子把五个无辜的人绑在电车轨道上。一辆失控的电车朝他们驶来，并且片刻后就要碾压到他们。幸运的是，你可以拉一个拉杆，让电车开到另一条轨道上。但是还有一个问题，那个疯子在那另一条轨道上也绑了一个人。考虑以上状况，你应该拉拉杆吗？',node=node)
new_topic.author = third_user
new_topic.last_reply = third_user
new_topic.num_views = 0
new_topic.num_replies = 0
new_topic.updated_on = datetime.datetime.now()
new_topic.save()
#初始化话题10
node = Node.objects.filter(name='Pythonic')[0]
node.num_topics += 1
node.save()
new_topic = Topic(title=u'史上最牛逼聊天插件',content=u'是暗红最牛逼聊天插件，使用chrome打开网页就能聊，不论你处于何时何地都能随时找到跟自己正在浏览同样网页的用户。筒子们，hight起来吧。安装办法：1. 点击下面的link下载插件2.打开chrome扩展程序（在工具--》扩展程序）3. 把你下载的文件拖进去，然后打开oschina的主页，然后点击右上角的那个中间有个蓝色的图标的东西，会出现让你聊天的内容啦！！记住，相同url的人可以在一起聊',node=node)
new_topic.author = new_user
new_topic.last_reply = new_user
new_topic.num_views = 0
new_topic.num_replies = 0
new_topic.updated_on = datetime.datetime.now()
new_topic.save()

#初始化回复1
second_reply = Reply(content=u'这是回复的内容')
second_reply.author = second_user
second_reply.topic = new_topic
second_reply.topic.num_replies += 1
second_reply.topic.updated_on = datetime.datetime.now()
second_reply.topic.last_reply = second_user
second_reply.topic.save()
second_reply.save()
#初始化回复2（回复的回复）
third_reply = Reply(content=u'你好！')
third_reply.author = new_user
third_reply.topic = new_topic
third_reply.topic.num_replies += 1
third_reply.topic.updated_on = datetime.datetime.now()
third_reply.topic.last_reply = new_user
third_reply.topic.save()
third_reply.has_parent = True
third_reply.parent = second_reply
third_reply.save()

#初始化私信1
time1 = datetime.datetime.now()
Message.objects.create(is_sender=True,talk_to=second_user,belong_to=new_user,content=u'Eric发出私信1',time=time1)
Message.objects.create(is_sender=False,talk_to=new_user,belong_to=second_user,content=u'Eric发出私信1',time=time1)
time2 = time1 + datetime.timedelta(seconds =10)
Message.objects.create(is_sender=True,talk_to=new_user,belong_to=second_user,content=u'Jack发出私信2',time=time2)
Message.objects.create(is_sender=False,talk_to=second_user,belong_to=new_user,content=u'Jack发出私信2',time=time2)
time3 = time2 + datetime.timedelta(seconds =10)
Message.objects.create(is_sender=True,talk_to=second_user,belong_to=new_user,content=u'Eric发出私信3',time=time3)
Message.objects.create(is_sender=False,talk_to=new_user,belong_to=second_user,content=u'Eric发出私信3',time=time3)
time4 = time3 + datetime.timedelta(seconds =10)
Message.objects.create(is_sender=True,talk_to=new_user,belong_to=second_user,content=u'Jack发出私信4',time=time4)
Message.objects.create(is_sender=False,talk_to=second_user,belong_to=new_user,content=u'Jack发出私信4',time=time4)
time5 = time4 + datetime.timedelta(seconds =10)
Message.objects.create(is_sender=True,talk_to=second_user,belong_to=new_user,content=u'Eric发出私信5',time=time5)
Message.objects.create(is_sender=False,talk_to=new_user,belong_to=second_user,content=u'Eric发出私信5',time=time5)
time6 = time5 + datetime.timedelta(seconds =10)
Message.objects.create(is_sender=True,talk_to=new_user,belong_to=second_user,content=u'Jack发出私信6',time=time6)
Message.objects.create(is_sender=False,talk_to=second_user,belong_to=new_user,content=u'Jack发出私信6',time=time6)
time7 = time6 + datetime.timedelta(seconds =10)
Message.objects.create(is_sender=True,talk_to=new_user,belong_to=second_user,content=u'Jack发出私信7',time=time7)
Message.objects.create(is_sender=False,talk_to=second_user,belong_to=new_user,content=u'Jack发出私信7',time=time7)
time8 = time7 + datetime.timedelta(seconds =10)
Message.objects.create(is_sender=True,talk_to=second_user,belong_to=new_user,content=u'Eric发出私信8',time=time8)
Message.objects.create(is_sender=False,talk_to=new_user,belong_to=second_user,content=u'Eric发出私信8',time=time8)


Site.objects.filter(id=1).update(domain='localhost:8000',name='Pythonic社区')