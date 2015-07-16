#-*-coding:utf-8 -*-
import logging

from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import translation
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from contact import contact
from generate_logs import functions as l_fct
from profil.functions import create_user
from profil.models import UserLang
from profil.forms.LogInForm import LogInForm
from profil.forms.RegisterForm import RegisterForm

logger_error = logging.getLogger('error')
logger_info = logging.getLogger('info')


def register_user(request):
    logger_info.info(l_fct.info_load_log_message(request))
    if request.user.is_authenticated():
        logger_error.error(l_fct.error_load_log_message(request))
        return redirect(
            request.META[
                'HTTP_REFERER'] if "HTTP_REFERER" in request.META else reverse('home'),
            permanent=True
        )
    else:
        errors = {}
        form = RegisterForm(request.POST)
        if request.method == 'POST' and len(request.POST):
            email_exist = User.objects.filter(email=request.POST['email'])
            user_exist = User.objects.filter(username=request.POST['username'])
            if len(user_exist) > 0:
                logger_error.error(l_fct.error_register_user_exist(request))
                errors['user'] = _("error_user_already_exist")
            if len(email_exist) > 0:
                logger_error.error(l_fct.error_register_mail_exist(request))
                errors['mail'] = _("error_mail_already_exist")
            if request.POST['password'] != request.POST['password_conf']:
                errors['pass'] = _("error_password")
            if len(errors) == 0 and form.is_valid():
                create_user(
                    request,
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                )
                UserLang(user=user, lang=translation.get_language()).save()
                redir = reverse('home')
                if 'next' in request.GET and request.GET['next'] != reverse('login'):
                    redir = request.GET['next']
                login(request, user)
                return redirect(
                    redir,
                    permanent=True
                )
            elif len(errors) == 0:
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
    logger_info.info(l_fct.info_load_log_message(request))
    return render(
        request,
        "profil/login.html",
        {
            'type': "select",
        }
    )


def login_user(request):
    logger_info.info(l_fct.info_load_log_message(request))
    if request.user.is_authenticated():
        logger_error.error(l_fct.error_load_log_message(request))
        return redirect(
            request.META[
                'HTTP_REFERER'] if "HTTP_REFERER" in request.META else reverse('home'),
            permanent=True
        )
    else:
        errors = {}
        form = LogInForm(request.POST)
        if request.method == 'POST' and len(request.POST):
            user_exist = User.objects.filter(username=request.POST['username'])
            if len(user_exist) == 0:
                logger_error.error(
                    l_fct.error_inexistant_user_log_message(request))
                errors['user'] = _("error_user_not_exist")
            else:
                if user_exist[0].is_superuser:
                    logger_error.error(
                        l_fct.error_login_admin_front_log_message())
                    errors['admin'] = _("admin_cant_log_here")
                elif user_exist[0].is_staff:
                    logger_error.error(
                        l_fct.error_login_staff_front_log_message())
                    errors['staff'] = _("staff_cant_log_here")
                if len(errors) == 0:
                    if 'user' not in errors:
                        user = authenticate(
                            username=request.POST['username'],
                            password=request.POST['password'],
                        )
                        if user is not None:
                            if user.is_active:
                                login(request, user)
                                userlang = UserLang.objects.get(
                                    user=request.user)
                                logger_info.info(
                                    l_fct.info_login_class_log_message(request))
                                translation.activate(userlang.lang)
                                request.session[
                                    translation.LANGUAGE_SESSION_KEY] = userlang.lang
                                request.session['ldap_connection'] = False
                                redir = reverse('home')
                                if 'HTTP_REFERER' in request.META and request.META['HTTP_REFERER'] != reverse('register'):
                                    redir = request.META['HTTP_REFERER']
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
                    else:
                        logger_error.error(
                            l_fct.error_login_unknow_log_message(request))
                        errors['unknow'] = _("unknow error")
    return render(
        request,
        "profil/login.html",
        {
            'form': form,
            'errors': errors,
            'type': "classic",
            'formcontact': contact.ContactForm(),
        }
    )


@login_required
def logout_user(request):
    logger_info.info(l_fct.info_load_log_message(request))
    if (request.user.is_staff or request.user.is_superuser) is not True:
        cur_language = translation.get_language()
        userlang = UserLang.objects.get(user=request.user)
        if userlang.lang is not cur_language:
            userlang.lang = cur_language
            userlang.save()
    redir = request.META[
        'HTTP_REFERER'] if "HTTP_REFERER" in request.META else reverse('home')
    if logout(request):
        logger_info.info(l_fct.info_logout_log_message(request))
    else:
        logger_error.info(l_fct.error_logout_log_message(request))
    return redirect(
        redir,
        permanent=True
    )
