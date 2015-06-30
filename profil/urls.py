from django.conf.urls import patterns
from django.conf.urls import url
from profil import views

urlpatterns = patterns('',
                       url(r'^register', views.register_user, name="register"),
                       url(r'^ldap', views.login_ldap, name="login_ldap"),
                       url(r'^login', views.login_user, name="login_classic"),
                       url(r'^logout', views.logout_user, name="logout"),
                       )
