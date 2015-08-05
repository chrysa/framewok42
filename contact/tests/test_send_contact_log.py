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
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import activate
from django.utils.translation import ugettext as _

from profil.models import UserLang


class ContactLogTests(TestCase):
    """
    this class define all unit tests for contact

    :param TestCase: librairy of unittest
    :type TestCase: object
    :return: None
    :rtype: None
    """

    def setUp(self):
        """
        set up variable and create user for the tests

        :param self: instance of ContactTests
        :type self: object
        :var self.client: instance of navigation client for tests
        :var self.register: dict for create new user
        :var new_user: instance of user contain new_user
        :return: None
        """
        self.client = Client()
        self.register_user = {'username': "user_test", 'email': 'user_test@tests.fr', 'password': "tests"}
        self.message_test = {'subject': 'mail unit tests', 'message': 'message de tests'}
        self.message_test_blank_subject = {'subject': '', 'message': 'message de tests'}
        self.message_test_blank_message = {'subject': 'mail unit tests', 'message': ''}
        self.message_test_blank_subject_message = {'subject': '', 'message': ''}
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        activate('fr')

    def test_send_contact_log(self):
        """
        tests send contact mail on log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.post(reverse('contact'), self.message_test)
        self.assertContains(reponse, _("contact_success"))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_send_contact_log_subject_blank(self):
        """
        tests send contact mail with blank subject on log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.post(reverse('contact'), self.message_test_blank_subject)
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_send_contact_log_message_blank(self):
        """
        tests send contact mail with blank subject on log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.post(reverse('contact'), self.message_test_blank_subject)
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_send_contact_log_blank_subject_message(self):
        """
        tests send contact mail with blank form on log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.post(reverse('contact'), self.message_test_blank_subject_message)
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertContains(reponse, _('contact_must_contain_message'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()
