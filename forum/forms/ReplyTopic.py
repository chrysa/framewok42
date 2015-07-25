#-*-coding:utf-8 -*-
"""
:module: forum.forms.ReplyTopic
:synopsis: generate the forum for reply of a topic

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 21/07/2015:
:seealso: forum.moodels.ForumPost
"""
from django import forms
from django.utils.translation import ugettext as _

from forum.models import ForumPost


class PostForm(forms.Form, forms.ModelForm):
    """
    this class define field of create topic form

    :param forms.Form: contain all function for define a field
    :type forms.Form: form object
    :param forms.ModelForm: contain all function for generate form from model
    :type forms.ModelForm: object
    :var content: content of topic
    :return: None
    :rtype: None
    """

    class Meta:
        model = ForumPost
        fields = [
            'Message',
        ]

    Message = forms.CharField(
        label=_("message"),
        widget=forms.Textarea(
            attrs={
                'class': "form-control",
                'placeholder': _("reponse")
            },
        ),
    )
