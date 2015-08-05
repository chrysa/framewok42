# -*-coding:utf-8 -*-
"""
:module: Issues.models
:synopsis: define storage models for issues

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 05/08/2015
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from autoslug import AutoSlugField


class Issue(models.Model):
    """define the storage of category

    :param models.Model: contain all function for define a storage
    :type models.Model: models object
    :var Autor: User object contain autor of request
    :var Assign: User object contain staff member in charge

    :return: Issue object
    :rtype: object
    """
    Autor = models.ForeignKey(User)
    Assign = models.ForeignKey(
        User,
        related_name=_("assign_to"),
        null=True,
    )
    Title = models.CharField(
        max_length=100
    )
    slug = AutoSlugField(populate_from='Title')
    UserRequest = models.TextField()
    Answer = models.TextField()
    CreateDate = models.DateTimeField(auto_now_add=True)
    LastActivity = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(
        max_length=20,
        default="open",
        choices=(
            ("open", _("open")),
            ("progress", _("in_progress")),
            ("close", _("status")),
        )
    )

    def __str__(self):
        return self.Title
