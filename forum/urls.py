# -*-coding:utf-8 -*-
"""
:module: forum.urls
:synopsis: root URL for forum

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 21/07/2015
:var urlpatterns: rooting of urls
"""
from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('forum.views',
                       url(r'^$', 'display_all', name="forum"),
                       url(r'^(?P<cat>.+)/create/$', 'create_topic', name="create_topic"),
                       url(r'^(?P<cat>.+)/(?P<topic>.+)/edit/(?P<post>.+)/$', 'edit_post', name="edit_post"),
                       url(r'^(?P<cat>.+)/edit/(?P<topic>.+)/$', 'edit_topic', name="edit_topic"),
                       url(r'^(?P<cat>.+)/reply/(?P<topic>.+)/$', 'reply_topic', name="send_reply"),
                       url(r'^(?P<cat>.+)/(?P<topic>.+)/$', 'display_topic', name="topic_cat"),
                       url(r'^(?P<cat>.+)/$', 'display_cat', name="cat"),
                       )
