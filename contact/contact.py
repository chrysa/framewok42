#-*-coding:utf-8 -*-
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from contact.forms.ContactFrom import ContactForm


def display(request):
    context = {
        'formcontact': ContactForm(),
    }
    return render(request, 'contact/contact.html', context)


def send_contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        send_mail(
            form.cleaned_data['subject'],
            form.cleaned_data['message'],
            form.cleaned_data['email'],
            ["greau.anthony@gmail.com"]
        )
    return redirect(
        request.META['HTTP_REFERER'] if "HTTP_REFERER" in request.META else reverse('home'),
        permanent=True
    )
