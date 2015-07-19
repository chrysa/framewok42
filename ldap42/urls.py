from django.conf.urls import patterns
from django.conf.urls import url

from ldap42 import views

urlpatterns = patterns('',
                       url(r'^$', views.login_ldap, name="login_ldap"),
                       url(r'^annuaire/(?P<order>.+)/(?P<letter>.+)/$', views.ldap_display, name="ldap_display_filter"),
                       )
