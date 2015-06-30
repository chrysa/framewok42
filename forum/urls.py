from django.conf.urls import patterns
from django.conf.urls import url
from forum import views

urlpatterns = patterns('',
                       url(r'^$', views.display_all, name="forum"),
                       url(r'^(?P<cat>.+)/create/$',views.create_topic, name="create_topic"),
                       url(r'^(?P<cat>.+)/(?P<topic>.+)/edit/(?P<post>.+)/$', views.edit_post, name="edit_post"),
                       url(r'^(?P<cat>.+)/edit/(?P<topic>.+)/$', views.edit_topic, name="edit_topic"),
                       url(r'^(?P<cat>.+)/reply/(?P<topic>.+)/$', views.reply_topic, name="send_reply"),
                       url(r'^(?P<cat>.+)/(?P<topic>.+)/$', views.display_topic, name="topic_cat"),
                       url(r'^(?P<cat>.+)/$', views.display_cat, name="cat"),
                       )
