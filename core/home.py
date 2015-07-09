# -*-coding:utf-8 -*-

import logging

from django.shortcuts import render

from core.functions import info_log_message


def index(request):
    logger = logging.getLogger('info')
    logger.info(info_log_message(request))
    return render(request, 'core/home.html', {})
