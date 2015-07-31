# -*-coding:utf-8 -*-
"""
:module: issues.urls
:synopsis: root URL for issues

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 21/07/2015
:var urlpatterns: rooting of urls
"""
from django.conf.urls import patterns
from django.conf.urls import url

from issues import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name="list_issue"),
                       url(r'^respond/(?P<issue>.+)/$',
                           views.respond_issue, name="respond_issue"),
                       url(r'^reopen/(?P<issue>.+)/$',
                           views.reopen_issue, name="reopen_issue"),
                       url(r'^view/(?P<issue>.+)/$',
                           views.view_issue, name="view_issue"),
                       url(r'^new_issue/$', views.new_issue, name="new_issue"),
                       )
