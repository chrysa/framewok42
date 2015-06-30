from django.conf.urls import patterns
from django.conf.urls import url
from core import home

urlpatterns = patterns('',
                       url(r'^', home.index, name="home"),
                       )
