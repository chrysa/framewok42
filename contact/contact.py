#-*-coding:utf-8 -*-
import logging

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from generate_logs.functions import info_load_log_message
from contact.forms.ContactFrom import ContactForm

logger_info = logging.getLogger('info')
logger_error = logging.getLogger('error')


def display(request):
    logger_info.info(info_load_log_message(request))
    context = {
        'formcontact': ContactForm(),
    }
    return render(request, 'contact/contact.html', context)


def send_contact(request):
    logger_info.info(info_load_log_message(request))
    form = ContactForm(request.POST)
    if form.is_valid():
        if send_mail(
            form.cleaned_data['subject'],
            form.cleaned_data['message'],
            form.cleaned_data['email'],
            ["greau.anthony@gmail.com"]
        ):
            logger_info.info(_("success_contact") + request.user)
        else:
            logger_error.error(_("error_contact") + request.user)
    return redirect(
        request.META['HTTP_REFERER'] if "HTTP_REFERER" in request.META else reverse('home'),
        permanent=True
    )
