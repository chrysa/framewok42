#-*-coding:utf-8 -*-
import datetime
import logging

from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

LOG_TYPE = [
    _('critical'),
    _('debug'),
    _('error'),
    _('log'),
    _('info'),
    _('warning'),
]

@login_required
def index(request):
    return render(
        request,
        'logs/index.html', {
            'type_log' : LOG_TYPE,
        }
    )

def add_log(type, mess):
    if type == "critical":
        logger.critical(mess)
    elif type == "debug":
        logger.debug(mess)
    elif type == "info":
        logger.info(mess)
    elif type == "error":
        logger.error(mess)
    elif type == "warning":
        logger.warning(mess)


# from datetime import datetime
# lines = (ligne.split(' :: ') for ligne in open('fichier.log'))
# errors = ((date, mes) for date, lvl, mes in lines if lvl in ('ERROR', 'CRITICAL'))
# before, after = datetime(2012, 1, 12), datetime(2012, 3, 24)
# parse = lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S,%f')
# dated_line = ((date, mes) for date, mess in errors if before <= parse(date) <= after)
# for date, message in dated_line:
#     print date, message
