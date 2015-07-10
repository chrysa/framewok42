#-*-coding:utf-8 -*-
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(
        request,
        'logs/index.html', {
            'type_log': [k for k, v in settings.LOGGING['handlers'].items() if k is not 'console'],
        }
    )


@login_required
def display_log(request, log_type):
    if not request.user.is_superuser:
        return redirect(request.META['HTTP_REFERER'])
    else:

        log = []
        len_ref = 0
        for ligne in open('logs/' + log_type + '.log'):
            split_ligne = ligne.split(' :: ')
            len_line = len(split_ligne)
            len_ref = len_line if not len_ref else len_ref
            if len_line == 2:
                split_ligne[0] = split_ligne[0].replace('[', '').replace(']', '').split(' ')
                split_ligne[1] = split_ligne[1].replace('\n', '').split(' by ')
            elif len_line == 3:
                split_ligne.remove(split_ligne[0])
                split_ligne[0] = split_ligne[0].replace('[', '').replace(']', '').split(' ')
                split_ligne[1] = split_ligne[1].replace(':', '/').replace('[', '').replace(']', '').split(' ')
                split_ligne[2] = split_ligne[2].replace('\n', '').split(' by ')
                split_ligne.append(split_ligne[2])
                split_ligne[2] = split_ligne[1]
                split_ligne[1] = split_ligne[3]
            elif len_line == 4:
                split_ligne[0] = split_ligne[0].replace('[', '').replace(']', '')
                split_ligne[1] = split_ligne[1].replace('[', '').replace(']', '').split(' ')
                split_ligne[2] = split_ligne[2].replace(':', '/').replace('[', '').replace(']', '').split(' ')
            log.append(split_ligne)
    return render(
        request,
        'logs/display_log.html', {
            'len': len_ref,
            'type': log_type,
            'log': log,
        }
    )
