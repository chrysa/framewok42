# -*-coding:utf-8 -*-
"""
:module: contact.contact
:synopsis: generate contact form

:moduleauthor: anthony geau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 27/07/2015
:var logger_error: logger error
:var logger_info: logger info
:seealso: django.core.mail.send_mail
:seealso: generate_logs.functions.info_load_log_message
:seealso: contact.forms.ContactFrom.ContactForm
"""
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.translation import ugettext as _

from generate_logs.functions import info_load_log_message
from contact.forms.ContactFrom import ContactForm

logger_error = logging.getLogger('error')
logger_info = logging.getLogger('info')


def display(request):
    """display contact form

    :param request: object contain context of request
    :type request: object
    :var errors: dict of process error
    :var success: dict of success process
    :var dump: dump to request.POST for set email whaen user log
    :var form: contain struct of contact form
    :return: HTTPResponse
    """
    logger_info.info(info_load_log_message(request))
    errors = {}
    success = {}
    if request.method == 'POST':
        dump = request.POST.copy()
        if 'email' not in dump:
            dump.appendlist('email', request.user.email)
        form = ContactForm(dump)
        if form.is_valid():
            try:
                admins = []
                for admin in settings.ADMINS:
                    admins.append(admin[1])
                send_mail(
                    form.cleaned_data['subject'],
                    form.cleaned_data['message'],
                    form.cleaned_data['email'],
                    admins
                )
                success['message'] = _('contact_success')
                logger_info.info(_("contact_success") + request.user.username)
            except:
                errors['message'] = _('contact_fail')
                logger_error.error(_("contact_fail") + request.user.username)
        else:
            if not request.POST['subject']:
                errors['subject'] = _('contact_must_contain_subject')
            if not request.POST['message']:
                errors['message'] = _('contact_must_contain_message')
            if not request.user.is_authenticated() and not request.POST['email']:
                errors['email'] = _('contact_must_contain_email')
    return render(
        request,
        'contact/contact.html', {
            'formcontact': ContactForm(request.POST),
            'errors': errors,
            'success': success
        }
    )
