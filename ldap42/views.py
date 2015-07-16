#-*-coding:utf-8 -*-
import ldap3
import logging

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

from contact import contact
from generate_logs import functions as l_fct
from ldap42.forms.LdapForm import LdapForm
from profil.functions import create_user
from profil.models import UserLang

logger_error = logging.getLogger('error')
logger_info = logging.getLogger('info')


@login_required
def annuaire(request, filter):
    return render(
        request,
        "ldap42/annuaire.html",
        {
            'filter': filter if filter else 'uid',
        }
    )


def login_ldap(request):
    logger_info.info(l_fct.info_load_log_message(request))
    if request.user.is_authenticated():
        logger_error.error(l_fct.error_load_log_message(request))
        return redirect(reverse('home'))
    else:
        errors = {}
        print(request.POST)
        form = LdapForm(request.POST)
        if request.method == 'POST':
            s = ldap3.Server(
                'ldaps://ldap.42.fr',
                port=636,
                get_info=ldap3.ALL
            )
            c = ldap3.Connection(
                s,
                auto_bind=True,
                client_strategy='SYNC',
                user='uid={},ou={},ou={},ou=paris,ou=people,dc=42,dc=fr'.format(request.POST['login'], request.POST['pool_month'], request.POST['pool_year']),
                password=request.POST['password'],
                authentication=ldap3.SIMPLE,
                check_names=True,
                raise_exceptions=False
            )
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
                u = User.objects.filter(username=c.response[0]['attributes']['uid'][0])
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
                        logger_info.info(l_fct.info_login_class_log_message(request))
                        translation.activate(userlang.lang)
                        request.session[translation.LANGUAGE_SESSION_KEY] = userlang.lang
                        request.session['ldap_connection'] = True
                        redir = reverse('home')
                        if 'HTTP_REFERER' in request.META and request.META['HTTP_REFERER'] != reverse('login'):
                            redir = request.META['HTTP_REFERER']
                        return redirect(
                            redir,
                            permanent=True
                        )
                    else:
                        logger_error.error(l_fct.error_login_log_message(request))
                        errors['unknow'] = _("authenticate error")
                else:
                    logger_error.error(l_fct.error_login_wrong_password_log_message(request))
                    errors['pass'] = _("error_wrong_password")
                c.unbind()
            else:
                logger_error.info(l_fct.error_ldap_log_message(request, "bind"))
                errors['unknow'] = _("bind_error")
        else:
            form = LdapForm()
    return render(
        request,
        "ldap42/loginldap.html",
        {
            'form': form,
            'errors': errors,
            'type': "ldap",
            'formcontact': contact.ContactForm(),
        }
    )
