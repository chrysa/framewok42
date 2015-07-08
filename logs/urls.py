from django.conf.urls import patterns
from django.conf.urls import url
from logs import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name="list_logs"),
                       )
