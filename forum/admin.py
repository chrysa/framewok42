# -- coding: utf-8 --#-*-coding:utf-8 -*-
"""
:module: forum.admin
:synopsis: define admin papnel for forum

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 21/07/2015:
:seealso: forum.moodels.ForumCat
:seealso: forum.moodels.ForumPost
:seealso: forum.moodels.ForumTopic
:todo: personalise admin panel
"""
from django.contrib import admin
from forum.models import ForumCat
from forum.models import ForumPost
from forum.models import ForumTopic

admin.site.register(ForumCat)
admin.site.register(ForumTopic)
admin.site.register(ForumPost)
