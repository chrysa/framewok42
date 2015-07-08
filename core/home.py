# -*-coding:utf-8 -*-

import logging

from django.shortcuts import render

def index(request):
    mess = "chargement de la page " + request.META['PATH_INFO']
    if request.user.is_authenticated():
        mess += " by " + request.user.username
    logger = logging.getLogger('info')
    logger.info(mess)
    return render(request, 'core/home.html', {})
