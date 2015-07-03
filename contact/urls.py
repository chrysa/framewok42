#-*-coding:utf-8 -*-
from django.conf.urls import patterns
from django.conf.urls import url
from contact import contact

urlpatterns = patterns('',
                       url(r'^contact', contact.display, name="contact"),
                       url(r'^send_contact', contact.send_contact,
                           name="send_contact"),
                       )
