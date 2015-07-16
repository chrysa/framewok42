#-*-coding:utf-8 -*-
import datetime

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class LdapForm(forms.Form, forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

    login = forms.CharField(
        label=_("login_user"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("login_user"),
            },
        ),
    )
    password = forms.CharField(
        label=_("password"),
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': _("password")
            },
        ),
    )

    pool_month = forms.ChoiceField(
        label=_("pool_month"),
        choices=[
            ('july', _('juillet')),
            ('august', _('aout')),
            ('september', _('septembre')),
            ('october', _('octobre'))
        ],
        widget=forms.Select(
            attrs={
                'class':'selector',
                'class': "form-control",
                'placeholder': _("pool_month")
            }
        ),
    )

    date_now = datetime.datetime.now()
    year = 2013
    years = []
    while year <= date_now.year:
        years.append((year, year))
        year += 1

    pool_year = forms.ChoiceField(
        label=_("pool_year"),
        choices=years,
        widget=forms.Select(
            attrs={
                'class':'selector',
                'class': "form-control",
                'placeholder': _("pool_year")
            }
        ),
    )