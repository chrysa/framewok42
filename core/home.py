# -*-coding:utf-8 -*-

import logging

from django.shortcuts import render
from django.utils import translation

from generate_logs.functions import info_load_log_message

def index(request):
    print(translation.get_language())
    logger = logging.getLogger('info')
    logger.info(info_load_log_message(request))
    return render(request, 'core/home.html', {})
