# -*-coding:utf-8 -*-

from django.shortcuts import render

from generate_logs.views import add_log

def index(request):
    mess = "chargement de la page " + request.META['PATH_INFO']
    if request.user.is_authenticated():
        mess += " by " + request.user.username
    add_log("info", mess)
    return render(request, 'core/home.html', {})
