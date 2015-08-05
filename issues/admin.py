#-*-coding:utf-8 -*-
"""
:module: issues.admin
:synopsis: define admin panel for issues

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 05/08/2015
:seealso: issues.moodels.Issue
:todo: personalise admin panel
"""
from django.contrib import admin

from issues.models import Issue


class IssueAdmin(admin.ModelAdmin):
    ordering = ['CreateDate', 'LastActivity', 'Status']
    list_display = (
    'Autor', 'Assign', 'short_title', 'short_userrequest', 'short_answer', 'CreateDate', 'LastActivity', 'Status')
    list_display_links = (
    'Autor', 'Assign', 'short_title', 'short_userrequest', 'short_answer', 'CreateDate', 'LastActivity', 'Status')
    list_filter = ('Autor', 'Assign', 'CreateDate', 'LastActivity', 'Status')
    search_fields = ['Autor', 'Assign', 'CreateDate', 'LastActivity', 'Status']

    def short_title(self, Issue):
        if len(Issue.Title) > 40:
            text = Issue.Title[0:40]
            return '{}…'.format(text)
        else:
            return Issue.Title

    def short_userrequest(self, Issue):
        if len(Issue.UserRequest) > 40:
            text = Issue.UserRequest[0:40]
            return '{}…'.format(text)
        else:
            return Issue.UserRequest

    def short_answer(self, Issue):
        if len(Issue.Answer) > 40:
            text = Issue.Answer[0:40]
            return '{}…'.format(text)
        else:
            return Issue.Answer


admin.site.register(Issue, IssueAdmin)
