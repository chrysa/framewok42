#-*-coding:utf-8 -*-
import logging

from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

LOG_TYPE = [
    _('critical'),
    _('error'),
    _('warning'),
    _('info'),
    _('debug')
]

@login_required
def index(request):
    print(LOG_TYPE)
    print(LOG_TYPE.sort())
    return render(
        request,
        'logs/index.html', {
            'type_log': LOG_TYPE.sort(),
        }
    )


def add_log(type, mess):
    logger = logging.getLogger(type)
    if type == 'critical':
        logger.critical(mess)
    elif type == 'error':
        logger.error(mess)
    elif type == 'warning':
        logger.warning(mess)
    elif type == 'info':
        logger.info(mess)
    elif type == 'debug':
        logger.debug(mess)


@login_required
def display_log(request):
    return
# from datetime import datetime
# lines = (ligne.split(' :: ') for ligne in open('fichier.log'))
# errors = ((date, mes) for date, lvl, mes in lines if lvl in ('ERROR', 'CRITICAL'))
# before, after = datetime(2012, 1, 12), datetime(2012, 3, 24)
# parse = lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S,%f')
# dated_line = ((date, mes) for date, mess in errors if before <= parse(date) <= after)
# for date, message in dated_line:
#     print date, message
