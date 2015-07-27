# -*-coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class RegisterForm(forms.Form, forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

    username = forms.CharField(
        required=True,
        label=_("username"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("username")
            },
        ),
    )
    email = forms.EmailField(
        required=True,
        label=_("mail_adress"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("mail_adress")
            },
        ),
    )
    password = forms.CharField(
        required=True,
        label=_("password"),
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': _("password")
            },
        ),
    )
    password_conf = forms.CharField(
        required=True,
        label=_("password_conf"),
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'placeholder': _("password_conf")
            },
        ),
    )
