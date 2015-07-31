# -*-coding:utf-8 -*-
"""
:module: contact.tests
:synopsis: unit testing for contact apps

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 22/07/2015
:seealso: profil.models.UserLang
"""
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from profil.models import UserLang


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
        :var new_user: instance of user contain new_user
        :return: None
        """
        self.client = Client()
        self.register_user = {
            'username': "user_test",
            'email': 'user_test@test.fr',
            'password': "test",
        }
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')

    def test_contact_url_unlog(self):
        """
        test access to url contact not log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('contact'))
        self.assertContains(reponse, _("mail_adress"))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def test_contact_url_log(self):
        """
        test access to url contact log status

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('contact'))
        self.assertNotContains(reponse, _("mail_adress"))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def send_contact_unlog(self):
        """
        test send contact mail on not log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('contact'),
                                  {'email': 'test@test.fr', 'subject': 'mail unit test', 'message': 'message de test'})
        self.assertContains(reponse, _("contact_success"))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def send_contact_log(self):
        """
        test send contact mail on log status

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user[
            'username'], password=self.register_user['password'])
        reponse = self.client.get(
            reverse('contact'), {'subject': 'mail unit test', 'message': 'message de test'})
        self.assertContains(reponse, _("contact_success"))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def send_contact_unlog_subject_vide(self):
        """
        test send contact mail with blank subject on not log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('contact'), {})
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def send_contact_unlog_mesage_vide(self):
        """
        test send contact mail with blank subject on not log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('contact'), {})
        self.assertContains(reponse, _('contact_must_contain_message'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def send_contact_unlog_vide_complet(self):
        """
        test send contact mail with blank form on not log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('contact'), {})
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertContains(reponse, _('contact_must_contain_message'))
        self.assertContains(reponse, _('contact_must_contain_email'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def send_contact_log_subject_vide(self):
        """
        test send contact mail with blank subject on log status

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user[
            'username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('contact'), {})
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def send_contact_log_mesage_vide(self):
        """
        test send contact mail with blank subject on log status

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user[
            'username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('contact'), {})
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def send_contact_log_vide_complet(self):
        """
        test send contact mail with blank form on log status

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user[
            'username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('contact'), {})
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertContains(reponse, _('contact_must_contain_message'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()
