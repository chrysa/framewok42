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
