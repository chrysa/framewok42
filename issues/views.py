# -*-coding:utf-8 -*-
"""
:module: issues.views
:synopsis: generate all content of issues

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 30/07/2015
:var logger_error: logger error
:var logger_info: logger info
:seealso: issues.models.Issue
:seealso: forum.forms.CreateTopic.TopicForm
:seealso: generate_logs.functions.info_load_log_message
:seealso: issues.forms.AdminResponseIssue.AdminResponseIssueForm
:seealso: from issues.forms.SubmitIssue.IssueFor
"""
import datetime
import logging

from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from issues.models import Issue
from generate_logs.functions import info_load_log_message
from issues.forms.AdminResponseIssue import AdminResponseIssueForm
from issues.forms.SubmitIssue import IssueForm

logger_info = logging.getLogger('info')


@login_required
def index(request):
    """display the issues about the user connected

    :param request: object contain context of request
    :type request: object
    :var issues: contain issues to display
    :return: HTTPResponse
    """
    logger_info.info(info_load_log_message(request))
    if request.user.is_superuser or request.user.is_staff:
        issues = Issue.objects.all()
    else:
        issues = Issue.objects.filter(Autor=request.user)
    return render(request, 'issues/home.html', {'issues': issues})

@login_required
def new_issue(request):
    logger_info.info(info_load_log_message(request))
    form = IssueForm(request.POST)
    context = {}
    if request.POST:
        if form.is_valid():
            create = Issue(
                Autor=request.user,
                Title=form.cleaned_data['Title'],
                UserRequest=form.cleaned_data['UserRequest'],
            ).save()
        if create is None:
            issue = Issue.objects.filter(
                Title=form.cleaned_data['Title']
            ).filter(
                Autor=request.user
            ).filter(
                UserRequest=form.cleaned_data['UserRequest']
            )[0]
            return redirect(
                reverse(
                    'view_issue',
                    kwargs={
                        'issue': issue.slug,
                    }
                ),
                permanent=True
            )
        else:
            context['error'] = _('save_error')
    context['form'] = form
    return render(request, 'issues/send_issue.html', context)

@login_required
def respond_issue(request, issue):
    logger_info.info(info_load_log_message(request))
    context = {}
    SelectIssue = Issue.objects.get(slug=issue)
    if request.POST:
        form = AdminResponseIssueForm(request.POST)
        if form.is_valid():
            Issue.objects.filter(
                slug=issue
            ).update(
                Assign=User.objects.get(username=form.cleaned_data['assign']),
                Answer=form.cleaned_data['answer'],
                Status=form.cleaned_data['status'],
                LastActivity=datetime.datetime.now()
            )
            return redirect(
                request.META['HTTP_REFERER'],
                permanent=True
            )
        else:
            context['error'] = _('update_error')
    form = AdminResponseIssueForm(
        {
            'assign': SelectIssue.Assign,
            'status': SelectIssue.Status,
            'answer': SelectIssue.Answer,
        }
    )
    context['form'] = form
    context['issue'] = SelectIssue
    return render(request, 'issues/issue_admin_response.html', context)

@login_required
def view_issue(request, issue):
    logger_info.info(info_load_log_message(request))
    context = {
        'issue': Issue.objects.get(slug=issue),
    }
    return render(request, 'issues/issue.html', context)

@login_required
def reopen_issue(request, issue):
    logger_info.info(info_load_log_message(request))
    issue = Issue.objects.filter(
        slug=issue
    )
    if issue.Status == 'close':
        issue.update(
            Status="open",
        )
    return redirect(
        reverse('list_issue'),
        permanent=True
    )
