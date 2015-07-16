from django.conf.urls import url

from ldap42 import views

urlpatterns = [
    url(r'^', views.login_ldap, name="login_ldap"),
    url(r'^annuaire/(?P<filter>.+)', views.annuaire, name="annuaire"),
]
