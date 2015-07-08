import logging

from django.conf import settings
from django.shortcuts import render


def index(request):
    mess = "chargement de la page " + request.META['PATH_INFO']
    if request.user.is_authenticated():
        mess += " by " + request.user.username
    settings.LOGGING['loggers']['core']['level'] = "INFO"
    logger = logging.getLogger(__name__)
    logger.info(mess)
    return render(request, 'core/home.html', {})
