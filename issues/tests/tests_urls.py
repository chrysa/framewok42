# -*-coding:utf-8 -*-
"""
:module: issues.tests.tests_urls
:synopsis: unit testing for issues urls

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 02/08/2015
:todo: tests admin acces
:todo: acces URL de reopen issue user connecte
:todo: acces URL de view conecte
:todo: acces URL de view non conecte
:todo: acces URL de new issue conecte
:todo: acces URL de new issue non conecte
:todo: tests affichage d'issue a vide
:todo: tests affichage d'issue créé par un seul user
:todo: tests affichage d'issue créé par plusieurs user
"""
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from profil.models import UserLang


class IssuesTests(TestCase):
    """
    this class define all unit tests for issues

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
        :var self.register_user: dict for create new user
        :return: None
        """
        self.client = Client()
        self.register_user = {'username': "user_test", 'email': 'user_test@tests.fr', 'password': "tests"}
        self.admin_datas = {'username': 'admin', 'password': 'admin'}
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')
        User.objects.create_user(**self.admin_datas)
        User.objects.filter(username=self.admin_datas['username']).update(is_staff=True, is_superuser=True)

    def test_url_list_issue_unlog(self):
        reponse = self.client.get(reverse('list_issue'))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('list_issue'))

    def test_url_list_issue_user_log(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('list_issue'))
        self.assertTemplateUsed(reponse, 'issues/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()
