#-*-coding:utf-8 -*-
"""
:module: core.urls
:synopsis: root URL for core

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 21/07/2015
:var urlpatterns: rooting of urls
"""
from django.conf.urls import patterns
from django.conf.urls import url
from core import home

urlpatterns = patterns('',
                       url(r'^', home.index, name="home"),
                       )
