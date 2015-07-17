#-*-coding:utf-8 -*-
import logging

from django.utils import translation
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

import generate_logs.functions as l_fct
from profil.models import UserLang

logger_error = logging.getLogger('error')
logger_info = logging.getLogger('info')


def create_user(request, username, email, password, first_name=None, last_name=None):
    User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    user = authenticate(
        username=username,
        password=password,
    )
    UserLang(user=user, lang=translation.get_language()).save()
    logger_info.info(l_fct.info_register_log_message(request))
