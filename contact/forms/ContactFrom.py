#-*-coding:utf-8 -*-

"""
:module: contact.form.ContactForm
:synopsis: generate contact form

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 21/07/2015
"""

from django import forms
from django.utils.translation import ugettext as _


class ContactForm(forms.Form):
    """
    this class define field of contact form
    :param forms.Form: contain all function for define a field
    :type forms.Form: form object
    :var email: define email field
    :var subject: define subject field
    :var message: define message field
    :return: None
    :rtype: None
    """
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
