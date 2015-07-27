# -*-coding:utf-8 -*-
"""
:module: contact.urls
:synopsis: root URL for contact

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 21/07/2015
:var urlpatterns: rooting of urls
"""
from django.conf.urls import patterns
from django.conf.urls import url

from contact import contact

urlpatterns = patterns('',
                       url(r'^contact', contact.display, name="contact"),
                       )
