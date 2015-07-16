#-*-coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from issues.models import Issue


class AdminResponseIssueForm(forms.Form):

    class Meta:
        model = Issue
        fields = [
            'Assign',
            'Answer',
            'Status',
        ]

    admin = User.objects.filter(is_superuser=True)
    USER_LIST = []
    for a in admin:
        USER_LIST.append((a, a))

    assign = forms.ChoiceField(
        label=_("assign"),
        choices=USER_LIST,
        widget=forms.Select(
            attrs={
                'class': 'selector',
                'class': "form-control",
                'placeholder': _("assign")
            }
        ),
    )
    status = forms.ChoiceField(
        label=_("status"),
        choices=(
            ("open", _("open")),
            ("progress", _("in progress")),
            ("close", _("close")),
        ),
        widget=forms.Select(
            attrs={
                'class': 'selector',
                'class': "form-control",
                'placeholder': _("status")
            }
        )
    )
    answer = forms.CharField(
        label=_("answer"),
        widget=forms.Textarea(
            attrs={
                'class': "form-control",
                'placeholder': _("answer")
            },
        ),
    )
