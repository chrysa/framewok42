# -*-coding:utf-8 -*-
"""
:module: contact.tests.test_send
:synopsis: unit testing sending contact for contact apps

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 01/08/2015
:seealso: profil.models.UserLang
:todo: doc
"""
from django.test import Client
from django.test import TestCase
from django.utils.translation import activate
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse


class ContactTests(TestCase):
    """
    this class define all unit test for contact

    :param TestCase: librairy of unittest
    :type TestCase: object
    :return: None
    :rtype: None
    """

    def setUp(self):
        """
        set up variable and create user for the test

        :param self: instance of ContactTests
        :type self: object
        :var self.client: instance of navigation client for test
        :var self.register: dict for create new user
        :return: None
        """
        self.client = Client()
        self.message = {'email': 'test@test.fr', 'subject': 'mail unit test', 'message': 'message de test'}
        self.message_blank_mail = {'email': '', 'subject': 'mail unit test', 'message': 'message de test'}
        self.message_blank_subject = {'email': 'test@test.fr', 'subject': '', 'message': 'message de test'}
        self.message_blank_message = {'email': 'test@test.fr', 'subject': 'mail unit test', 'message': ''}
        self.message_blank_email_subject = {'email': '', 'subject': '', 'message': 'message de test'}
        self.message_blank_email_message = {'email': '', 'subject': 'mail unit test', 'message': ''}
        self.message_blank_subject_message = {'email': 'test@test.fr', 'subject': '', 'message': ''}
        self.message_all_blank = {'email': '', 'subject': '', 'message': ''}
        activate('fr')

    def test_send_contact_unlog(self):
        """
        test send contact mail on not log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.post(reverse('contact'), self.message)
        self.assertContains(reponse, _("contact_success"))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def test_send_contact_unlog_blank_mail(self):
        reponse = self.client.post(reverse('contact'), self.message_blank_mail)
        self.assertContains(reponse, _('contact_must_contain_email'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def test_send_contact_unlog_blank_subject(self):
        """
        test send contact mail with blank subject on not log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.post(reverse('contact'), self.message_blank_subject)
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def test_send_contact_unlog_blank_message(self):
        """
        test send contact mail with blank subject on not log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.post(reverse('contact'), self.message_blank_message)
        self.assertContains(reponse, _('contact_must_contain_message'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def test_send_contact_unlog_blank_email_subject(self):
        reponse = self.client.post(reverse('contact'), self.message_blank_email_subject)
        self.assertContains(reponse, _('contact_must_contain_email'))
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def test_send_contact_unlog_blank_email_message(self):
        reponse = self.client.post(reverse('contact'), self.message_blank_email_message)
        self.assertContains(reponse, _('contact_must_contain_email'))
        self.assertContains(reponse, _('contact_must_contain_message'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def test_send_contact_unlog_blank_subject_message(self):
        reponse = self.client.post(reverse('contact'), self.message_blank_subject_message)
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertContains(reponse, _('contact_must_contain_message'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def test_send_contact_unlog_all_blank(self):
        """
        test send contact mail with blank form on not log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.post(reverse('contact'), self.message_all_blank)
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertContains(reponse, _('contact_must_contain_message'))
        self.assertContains(reponse, _('contact_must_contain_email'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)


