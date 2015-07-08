#-*-coding:utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _

from forum.models import ForumPost


class PostForm(forms.Form, forms.ModelForm):

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
