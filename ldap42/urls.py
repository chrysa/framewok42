from django.conf.urls import patterns
from django.conf.urls import url

from ldap42 import views

urlpatterns = patterns('',
    url(r'^', views.login_ldap, name="login_ldap"),
                       url(r'^annuaire', views.annuaire, name="annuaire"),
                       url(r'^annuaire/(?P<filter>.+)', views.annuaire, name="annuaire_filter"),
                       )
