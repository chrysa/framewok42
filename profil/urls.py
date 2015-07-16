from django.conf.urls import url
from profil import views

urlpatterns = [
   url(r'^register', views.register_user, name="register"),
   url(r'^login', views.select_login, name="login"),
   url(r'^local', views.login_user, name="login_classic"),
   url(r'^logout', views.logout_user, name="logout"),
]
