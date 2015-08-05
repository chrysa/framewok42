# -*-coding:utf-8 -*-
"""
:module: contact.tests.tests_urls
:synopsis: unit testing urls for contact apps

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 31/07/2015
:seealso: profil.models.UserLang
"""
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from profil.models import UserLang


class ContactUrlUnLogTests(TestCase):
    """
    this class define all unit tests for contact

    :param TestCase: librairy of unittest
    :type TestCase: object
    :return: None
    :rtype: None
    """

    def test_contact_url_unlog(self):
        """
        tests access to url contact not log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('contact'))
        self.assertContains(reponse, _("mail_adress"))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)


class ContactUrlLogTests(TestCase):
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
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')


    def test_contact_url_log(self):
        """
        tests access to url contact log status

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('contact'))
        self.assertNotContains(reponse, _("mail_adress"))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()
