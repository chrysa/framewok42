# -*-coding:utf-8 -*-

import logging

from django.shortcuts import render

from generate_logs.functions import info_load_log_message

logger = logging.getLogger('info')


def index(request):
    logger.info(info_load_log_message(request))
    return render(request, 'core/home.html', {})
