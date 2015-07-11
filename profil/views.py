#-*-coding:utf-8 -*-
import ldap3
import logging

from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import translation
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from contact import contact
from profil.models import UserLang
from generate_logs.functions import info_load_log_message
from generate_logs.functions import info_login_class_log_message
from generate_logs.functions import info_login_ldap_log_message
from generate_logs.functions import info_logout_log_message
from generate_logs.functions import info_register_log_message
from profil.forms.LdapForm import LdapForm
from profil.forms.LogInForm import LogInForm
from profil.forms.RegisterForm import RegisterForm

logger_error = logging.getLogger('error')
logger_info = logging.getLogger('info')

def register_user(request):
    logger_info.info(info_load_log_message(request))
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    else:
        errors = {}
        form = RegisterForm(request.POST)
        if request.method == 'POST':
            email_exist = User.objects.filter(email=request.POST['email'])
            if form.is_valid():
                if len(email_exist) > 0:
                    errors['mail'] = _("error_mail_already_exist")
                elif form.cleaned_data['password'] != form.cleaned_data['password_conf']:
                    errors['pass'] = _("error_password")
                if 'mail' not in errors and 'pass' not in errors:
                    User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password']
                    )
                    user = authenticate(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'],
                    )
                    UserLang(user=user, lang=translation.get_language()).save()
                    logger_info.info(info_register_log_message(request))
                    redir = reverse('home')
                    if request.GET['next'] != reverse('register'):
                        redir = request.GET['next']
                    login(request, user)
                    return redirect(
                        redir,
                        permanent=True
                    )
            else:
                user_exist = User.objects.filter(username=request.POST['username'])
                if len(user_exist) > 0:
                    errors['user'] = _("error_user_already_exist")
                if len(email_exist) > 0:
                    errors['mail'] = _("error_mail_already_exist")
                if request.POST['password'] != request.POST['password_conf']:
                    errors['pass'] = _("error_password")
                if not len(errors):
                    errors['form'] = _("unknow_error_register_form")
        return render(
            request,
            "profil/register.html",
            {
                'form': form,
                'errors': errors,
                'formcontact': contact.ContactForm(),
            }
        )


def select_login(request):
    logger_info.info(info_load_log_message(request))
    return render(
        request,
        "profil/login.html",
        {
            'type': "select",
        }
    )

def login_user(request):
    logger_info.info(info_load_log_message(request))
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    else:
        error = {}
        if request.method == 'POST':
            form = LogInForm(request.POST)
            if request.POST['username'] == "admin":
                error['admin'] = _("admin_cant_log_here")
            else:
                user_exist = User.objects.filter(username=request.POST['username'])
                if len(user_exist) == 0:
                    error['user'] = _("error_user_not_exist")
                if 'user' not in error:
                    user = authenticate(
                        username=request.POST['username'],
                        password=request.POST['password'],
                    )
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            userlang = UserLang.objects.get(user=request.user)
                            logger_info.info(info_login_class_log_message(request))
                            translation.activate(userlang.lang)
                            request.session[translation.LANGUAGE_SESSION_KEY] = userlang.lang
                            redir = reverse('home')
                            if request.GET['next'] != reverse('login_classic') or request.GET['next'] != reverse('login_ldap') or request.GET['next'] != reverse('login'):
                                redir = request.GET['next']
                            return redirect(
                                redir,
                                permanent=True
                            )
                        else:
                            error['unknow'] = _("authenticate error")
                    else:
                        error['pass'] = _("error_wrong_password")
                else:
                    error['unknow'] = _("unknow error")
        else:
            form = LogInForm()
    return render(
        request,
        "profil/login.html",
        {
            'form': form,
            'error': error,
            'type': "classic",
            'formcontact': contact.ContactForm(),
        }
    )


def login_ldap(request):
    logger_info.info(info_load_log_message(request))
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    else:
        error = {}
        form = LdapForm(request.POST)
        if request.method == 'POST':
            try:
                s = ldap3.Server(
                    'ldaps://ldap.42.fr',
                    port=636,
                    get_info=ldap3.ALL
                )
                c = ldap3.Connection(
                    s,
                    auto_bind=True,
                    client_strategy='SYNC',
                    user='uid={},ou=july,ou=2013,ou=paris,ou=people,dc=42,dc=fr'.format(request.POST['login']),
                    password=request.POST['password'],
                    authentication=ldap3.SIMPLE,
                    check_names=True,
                    raise_exceptions=False
                )
                if c.bind():
                    logger_info.info(info_login_class_log_message(request))
                    c.search(
                        search_base='ou=people,dc=42,dc=fr',
                        search_filter='(uid={})'.format(request.POST['login']),
                        search_scope=ldap3.SUBTREE,
                        attributes=[
                            'sn',
                            'objectClass',
                        ]
                    )
                    response = c.response
                    for r in response:
                        print(r['attributes'])
                    c.unbind()
            except:
                error['unknow'] = _("bind_error")
        else:
            form = LdapForm()
    return render(
        request,
        "profil/login.html",
        {
            'form': form,
            'error': error,
            'type': "ldap",
            'formcontact': contact.ContactForm(),
        }
    )


@login_required
def logout_user(request):
    logger_info.info(info_load_log_message(request))
    if request.user.is_staff is not True:
        cur_language = translation.get_language()
        userlang = UserLang.objects.get(user=request.user)
        if userlang.lang is not cur_language:
            userlang.lang = cur_language
            userlang.save()
    redir = request.META['HTTP_REFERER'] if "HTTP_REFERER" in request.META else reverse('home')
    if logout(request):
        logger_info.info(info_logout_log_message(request))
    else:
        logger_error.info(info_logout_log_message(request))
    return redirect(
        redir,
        permanent=True
    )
