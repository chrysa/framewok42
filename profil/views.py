#-*-coding:utf-8 -*-
import ldap3

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
from profil.forms.LogInForm import LogInForm
from profil.forms.RegisterForm import RegisterForm
from profil.models import UserLang


def register_user(request):
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
                redir = reverse('home')
                if "HTTP_REFERER" in request.META:
                    redir = reverse('home') if request.META['PATH_INFO'] == reverse('register') else request.META['PATH_INFO']
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


def login_user(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    else:
        error = {}
        form = LogInForm(request.POST)
        if request.method == 'POST':
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
                        translation.activate(userlang.lang)
                        request.session[translation.LANGUAGE_SESSION_KEY] = userlang.lang
                        return redirect(
                            request.META['HTTP_REFERER'] if "HTTP_REFERER" in request.META else reverse('home'),
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
            'formcontact': contact.ContactForm(),
        }
    )

def login_ldap(request):
    user = 'agreau'
    password  = "mCKb0ss#123"
    s = ldap3.Server(
        host='ldap.42.fr',
        port=636,
        use_ssl=True,
        get_info='ALL'
    )
    c = ldap3.Connection(
        s,
        user='uid=%s,ou=2013,ou=2014,ou=people,dc=42,dc=fr' % user,
        password=password,
        auto_bind='NONE',
        version=3,
        authentication='SIMPLE',
        client_strategy = 'SYNC',
        auto_referrals=True,
        check_names=True,
        read_only=False,
        lazy=False,
        raise_exceptions=False
    )
    if not c.bind():
        print('error in bind', c.result)
    # username = "uid=agreau,ou=2013,ou=2014, ou=people,dc=42,dc=fr"
    # password  = "mCKb0ss#123"

    # Any errors will throw an ldap.LDAPError exception
    # or related exception so you can ignore the result

@login_required(login_url='/profil/login')
def logout_user(request):
    if request.user.is_staff is not True:
        cur_language = translation.get_language()
        userlang = UserLang.objects.get(user=request.user)
        if userlang.lang is not cur_language:
            userlang.lang = cur_language
            userlang.save()
    redir = request.META['HTTP_REFERER'] if "HTTP_REFERER" in request.META else reverse('home')
    logout(request)
    return redirect(
        redir,
        permanent=True
    )
