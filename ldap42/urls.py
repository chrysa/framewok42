from django.conf.urls import url
from ldap42 import views

urlpatterns = [
    url(r'^ldap', views.login_ldap, name="login_ldap"),
]
