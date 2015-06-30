#-*-coding:utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from issues.models import Issue

class IssueForm(forms.Form):

    class Meta:
        model = Issue
        fields = [
            'Title',
            'UserRequest',
        ]

    Title = forms.CharField(
        label=_("title"),
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': _("title")
            },
        ),
    )
    UserRequest = forms.CharField(
        label=_("issue"),
        widget=forms.Textarea(
            attrs={
                'class': "form-control",
                'placeholder': _("issue")
            },
        ),
    )
