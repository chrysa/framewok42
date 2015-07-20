from django.conf.urls import patterns
from django.conf.urls import url

from generate_logs import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name="list_logs"),
                       url(r'^(?P<log_type>.+)/$', views.display_log, name="view_log"),
                       )
