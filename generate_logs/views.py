# -*-coding:utf-8 -*-
"""
:module: generate_logs.views
:synopsis: generate all content of forum

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 30/07/2015
:seealso: generate_logs.functions.info_load_log_message
"""
import logging

from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from generate_logs.functions import info_load_log_message

logger_info = logging.getLogger('info')
logger_error = logging.getLogger('error')


@login_required
def index(request):
    """display select logs

    :param request: object contain context of request
    :type request: object
    :return: HTTPResponse
    """
    if not request.user.is_superuser:
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else reverse('home'))
    else:
        logger_info.info(info_load_log_message(request))
        return render(
            request,
            'logs/index.html', {
                'type_log': [k for k, v in settings.LOGGING['handlers'].items() if k is not 'console'],
            }
        )


@login_required
def display_log(request, log_type):
    """parse and display selected log

    :param request: object contain context of request
    :type request: object
    !param log_tyoe: log type to display
    :typer log_type: string
    :return: HTTPResponse
    """
    logger_info.info(info_load_log_message(request))
    if not request.user.is_superuser:
        return redirect(request.META['HTTP_REFERER'] if 'HTTP_REFERER' in request.META else reverse('home'))
    else:
        if log_type in settings.LOGGING['handlers'].keys() and log_type != 'console':
            type_format = settings.LOGGING['handlers'][log_type]['formatter']
            log = []
            try:
                file = open('logs/' + log_type + '.log')
                for ligne in file:
                    split_ligne = ligne.split(' :: ')
                    if type_format == 'simple':
                        split_ligne[0] = split_ligne[0].replace(
                        '[', '').replace(']', '').split(' ')
                        split_ligne[1] = split_ligne[
                            1].replace('\n', '').split(' par ')
                        add = True
                    elif type_format == 'verbose':
                        try:
                            split_ligne[0] = split_ligne[0].replace(
                                '[', '').replace(']', '').split(' ')
                            split_ligne[1] = split_ligne[1].replace(
                                ':', '.').replace('[', '').replace(']', '').split(' ')
                            split_ligne[2] = split_ligne[
                                2].replace('\n', '').split(' par ')
                            add = True
                        except:
                            add = False
                    elif type_format == 'complet':
                        try:
                            split_ligne[0] = split_ligne[
                                0].replace('[', '').replace(']', '')
                            split_ligne[1] = split_ligne[1].replace(
                                '[', '').replace(']', '').split(' ')
                            split_ligne[2] = split_ligne[2].replace(
                                ':', '.').replace('[', '').replace(']', '').split(' ')
                            split_ligne[3] = split_ligne[
                                3].replace('\n', '').split(' par ')
                            split_ligne.append(split_ligne[2])
                            split_ligne[2] = split_ligne[3]
                            split_ligne[3] = split_ligne[4]
                            split_ligne.remove(split_ligne[4])
                            add = True
                        except:
                            add = False
                    if add:
                        log.append((len(split_ligne), split_ligne))
                if len(log) > 1:
                    log.reverse()
            except:
                logger_error.error('error_load_log_{}'.format(log_type))
            return render(
                request,
                'logs/display_log.html', {
                    'type_format': type_format,
                    'all_type_log': [k for k, v in settings.LOGGING['handlers'].items() if k is not 'console'],
                    'type_log': log_type,
                    'len': len(log),
                    'log': log,
                }
            )
        else:
            return redirect(reverse('list_logs'))