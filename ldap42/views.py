# -*-coding:utf-8 -*-

import base64
import logging
import string
from operator import itemgetter

import ldap3
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import translation
from django.contrib.auth import authenticate
from django.contrib.auth import hashers
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.utils.translation import ugettext as _

from generate_logs import functions as l_fct
from ldap42.forms.LdapForm import LdapForm
from profil.functions import create_user
from profil.models import UserLang

logger_error = logging.getLogger('error')
logger_info = logging.getLogger('info')


def connect_to_ldap(session):
    s = ldap3.Server(
        'ldaps://ldap.42.fr',
        port=636,
        get_info=ldap3.ALL
    )
    c = ldap3.Connection(
        s,
        auto_bind=True,
        client_strategy='SYNC',
        user='uid={},ou={},ou={},ou=paris,ou=people,dc=42,dc=fr'.format(session['ldap_log']['login'],
                                                                        session['ldap_log'][
                                                                            'pool_month'],
                                                                        session['ldap_log']['pool_year']),
        password=session['ldap_log']['password'],
        authentication=ldap3.SIMPLE,
        check_names=True,
        raise_exceptions=False
    )
    return c


@login_required
def ldap_display(request, order, letter):
    logger_info.info(l_fct.info_load_log_message(request))
    errors = []
    alphabet = string.ascii_lowercase
    if letter != 'all' and letter not in alphabet:
        l = 'a'
    elif letter == 'all':
        l = ''
    else:
        l = letter
    c = connect_to_ldap(request.session)
    if c.bind():
        logger_info.info(l_fct.info_login_ldap_log_message(request))
        c.search(
            search_base='ou=paris,ou=people,dc=42,dc=fr',
            search_filter='(uid={}*)'.format(l),
            search_scope=ldap3.SUBTREE,
            attributes=[
                'uid',
                'givenName',
                'jpegPhoto',
                'mobile',
                'sn',
            ]
        )
        annuaire = []
        for r in c.response:
            annuaire.append(
                {
                    'avatar': base64.b64encode(r['attributes']['jpegPhoto'][0]) if 'jpegPhoto' in r[
                        'attributes'] else '',
                    'uid': r['attributes']['uid'][0],
                    'givenName': r['attributes']['givenName'][0],
                    'mobile': r['attributes']['mobile'][0] if 'mobile' in r['attributes'] else '',
                    'sn': r['attributes']['sn'][0],
                }
            )
        c.unbind()
        annuaire.sort(
            key=itemgetter('uid'), reverse=True if order == 'reverse' else False)
    else:
        logger_error.info(l_fct.error_ldap_log_message(request, "bind"))
        errors['unknow'] = _("bind_error")
    return render(
        request,
        "ldap42/ldap_display.html",
        {
            'alphabet': alphabet,
            'annuaire': annuaire,
            'form': LdapForm(),
            'letter': letter,
            'order': order,
        }
    )


def login_ldap(request):
    logger_info.info(l_fct.info_load_log_message(request))
    if request.user.is_authenticated():
        logger_error.error(l_fct.error_load_log_message(request))
        return redirect(reverse('home'))
    else:
        errors = {}
        form = LdapForm(request.POST)
        if request.method == 'POST':
            request.session['ldap_log'] = request.POST
            c = connect_to_ldap(request.session)
            if c.bind():
                logger_info.info(l_fct.info_login_ldap_log_message(request))
                c.search(
                    search_base='ou=people,dc=42,dc=fr',
                    search_filter='(uid={})'.format(request.POST['login']),
                    search_scope=ldap3.SUBTREE,
                    attributes=[
                        'uid',
                        'givenName',
                        'mobile',
                        'sn',
                        'alias'
                    ]
                )
                u = User.objects.filter(
                    username=c.response[0]['attributes']['uid'][0])
                if len(u) == 0:
                    create_user(
                        request,
                        c.response[0]['attributes']['uid'][0],
                        c.response[0]['attributes']['alias'][0],
                        request.POST['password'],
                        c.response[0]['attributes']['givenName'][0],
                        c.response[0]['attributes']['sn'][0],
                    )
                else:
                    if not hashers.check_password(request.POST['password'], u[0].password):
                        u[0].set_password(request.POST['password'])
                        u[0].save()
                user = authenticate(
                    username=request.POST['login'],
                    password=request.POST['password'],
                )
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        userlang = UserLang.objects.get(user=request.user)
                        logger_info.info(
                            l_fct.info_login_class_log_message(request))
                        translation.activate(userlang.lang)
                        request.session[
                            translation.LANGUAGE_SESSION_KEY] = userlang.lang
                        redir = reverse('home')
                        if 'next' in request.GET and request.GET['next'] != reverse('login'):
                            redir = request.GET['next']
                        return redirect(
                            redir,
                            permanent=True
                        )
                    else:
                        logger_error.error(
                            l_fct.error_login_log_message(request))
                        errors['unknow'] = _("authenticate error")
                else:
                    logger_error.error(
                        l_fct.error_login_wrong_password_log_message(request))
                    errors['pass'] = _("error_wrong_password")
                c.unbind()
            else:
                logger_error.info(
                    l_fct.error_ldap_log_message(request, "bind"))
                errors['unknow'] = _("bind_error")
        else:
            form = LdapForm()
    return render(
        request,
        "ldap42/loginldap.html",
        {
            'form': form,
            'errors': errors,
        }
    )
