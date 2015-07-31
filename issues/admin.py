#-*-coding:utf-8 -*-
"""
:module: forum.admin
:synopsis: define admin panel for forum

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 21/07/2015
:seealso: issues.moodels.Issue
:todo: personalise admin panel
"""
from django.contrib import admin

from issues.models import Issue

admin.site.register(Issue)
