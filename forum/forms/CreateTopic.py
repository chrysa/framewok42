# -*-coding:utf-8 -*-
"""
:module: forum.forms.CreateTopic
:synopsis: generate the forum for create a new topic

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 21/07/2015
:seealso: forum.moodels.ForumTopic
"""
from django import forms
from django.utils.translation import ugettext as _

from forum.models import ForumTopic


class TopicForm(forms.Form, forms.ModelForm):
    """
    this class define field of create topic form

    :param forms.Form: contain all function for define a field
    :type forms.Form: form object
    :param forms.ModelForm: contain all function for generate form from model
    :type forms.ModelForm: object
    :var title: title of topic
    :var content: content of topic
    :return: None
    :rtype: None
    """

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
