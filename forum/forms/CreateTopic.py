#-*-coding:utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from forum.models import ForumTopic


class TopicForm(forms.Form, forms.ModelForm):

    class Meta:
        model = ForumTopic
        fields = [
            'Title',
            'Message',
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

    Message = forms.CharField(
        label=_("message"),
        widget=forms.Textarea(
            attrs={
                'class': "form-control",
                'placeholder': _("message")
            },
        ),
    )
