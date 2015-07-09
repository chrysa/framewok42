#-*-coding:utf-8 -*-
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

LOG_TYPE = [
    _('critical'),
    _('error'),
    _('warning'),
    _('info'),
    _('debug'),
    _('general_log')
]


@login_required
def index(request):
    return render(
        request,
        'logs/index.html', {
            'type_log': LOG_TYPE,
        }
    )


@login_required
def display_log(request, log_type):
    if not request.user.is_superuser:
        return redirect(request.META['HTTP_REFERER'])
    else:
        log = []
        for ligne in open('logs/' + log_type + '.log'):
            split_ligne = ligne.split(' :: ')
            if len(split_ligne) == 2:
                split_ligne[0] = split_ligne[0].split(' ')
                split_ligne[0][0] = split_ligne[0][0].replace('[', '')
                split_ligne[0][1] = split_ligne[0][1].replace(']', '')
                split_ligne[1] = split_ligne[1].replace('\n', '').split(' by ')
            elif len(split_ligne) == 4:
                split_ligne.remove(split_ligne[0])
                split_ligne[0] = split_ligne[0].split(' ')
                split_ligne[0][0] = split_ligne[0][0].replace('[', '')
                split_ligne[0][1] = split_ligne[0][1].replace(']', '')
                split_ligne[1] = split_ligne[1].replace(
                    ':', '/').replace('[', '').replace(']', '')
                split_ligne[1] = split_ligne[1].split(' ')
                split_ligne[2] = split_ligne[2].replace('\n', '').split(' by ')

                split_ligne.append(split_ligne[2])
                split_ligne[2] = split_ligne[1]
                split_ligne[1] = split_ligne[3]
            print(split_ligne)
            log.append(split_ligne)
    return render(
        request,
        'logs/display_log.html', {
            'type': log_type,
            'log': log,
        }
    )
