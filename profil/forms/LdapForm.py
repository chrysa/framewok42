#-*-coding:utf-8 -*-
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
