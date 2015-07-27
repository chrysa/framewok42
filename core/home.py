# -*-coding:utf-8 -*-
"""
:module: core.home
:synopsis: generate contact form

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 21/07/2015:
:var logger_error: logger error
:var logger_info: logger info
"""

import logging

from django.shortcuts import render

from generate_logs.functions import info_load_log_message

logger = logging.getLogger('info')


def index(request):
    """home page

    :param request: object contain context of request
    :type request: object
    :seealso: contact.forms.ContactFrom.ContactForm
    :return: HTTPResponse
    """
    logger.info(info_load_log_message(request))
    return render(request, 'core/home.html', {})
