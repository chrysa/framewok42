#-*-coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class LogInForm(forms.Form, forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

    username = forms.CharField(
        label=_("username"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("username"),
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
