#-*-coding:utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _


class ContactForm(forms.Form):
    email = forms.EmailField(
        label=_("mail_adress"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("mail_adress")
            },
        ),
    )
    subject = forms.CharField(
        label=_("subject"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("subject")
            },
        ),
    )
    message = forms.CharField(
        label=_("message"),
        widget=forms.Textarea(
            attrs={
                'class': "form-control",
                'placeholder': _("message")
            },
        ),
    )
