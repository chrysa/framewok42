#-*-coding:utf-8 -*-
import logging

from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from generate_logs.functions import info_load_log_message

logger_info = logging.getLogger('info')


@login_required
def index(request):
    logger_info.info(info_load_log_message(request))
    return render(
        request,
        'logs/index.html', {
            'type_log': [k for k, v in settings.LOGGING['handlers'].items() if k is not 'console'],
        }
    )


@login_required
def display_log(request, log_type):
    logger_info.info(info_load_log_message(request))
    if not request.user.is_superuser:
        return redirect(request.META['HTTP_REFERER'])
    else:
        type_format = settings.LOGGING['handlers'][log_type]['formatter']
        log = []
        for ligne in open('logs/' + log_type + '.log'):
            split_ligne = ligne.split(' :: ')
            if type_format == 'simple':
                split_ligne[0] = split_ligne[0].replace(
                    '[', '').replace(']', '').split(' ')
                split_ligne[1] = split_ligne[
                    1].replace('\n', '').split(' par ')
                add = True
            elif type_format == 'verbose':
                split_ligne[0] = split_ligne[0].replace(
                    '[', '').replace(']', '').split(' ')
                split_ligne[1] = split_ligne[1].replace(
                    ':', '.').replace('[', '').replace(']', '').split(' ')
                split_ligne[2] = split_ligne[
                    2].replace('\n', '').split(' par ')
                print(split_ligne)
                add = True
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
                log.append(split_ligne)
        if len(log) > 1:
            log.reverse()
    return render(
        request,
        'logs/display_log.html', {
            'type_format': type_format,
            'type_log': log_type,
            'len': len(log),
            'log': log,
        }
    )
