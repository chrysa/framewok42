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


class UrlIssuesTestsUnLog(TestCase):
    def test_url_list_issue_unlog(self):
        reponse = self.client.get(reverse('list_issue'))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('list_issue'))

    # def test_url_respond_issue_unlog(self):
    #     reponse = self.client.get(reverse('respond_issue'))
    #     self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('respond_issue'))

    # def test_url_reopen_issue_unlog(self):
    #     reponse = self.client.get(reverse('reopen_issue'))
    #     self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('reopen_issue'))

    # def test_url_view_issue_unlog(self):
    #     reponse = self.client.get(reverse('view_issue'))
    #     self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('view_issue'))

    def test_url_new_issue_unlog(self):
        reponse = self.client.get(reverse('new_issue'))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('new_issue'))


class UrlIssuesTestsLog(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_user = {'username': "user_test", 'email': 'user_test@tests.fr', 'password': "tests"}
        self.register_admin = {'username': 'admin', 'email': 'admin@admin.fr', 'password': 'admin'}
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')
        new_admin = User.objects.create_user(**self.register_admin)
        User.objects.filter(username=self.register_admin['username']).update(is_staff=True, is_superuser=True)
        UserLang.objects.create(user=new_admin, lang='fr')

    def test_url_list_issue_unlog(self):
        reponse = self.client.get(reverse('list_issue'))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('list_issue'))

    # def test_url_respond_issue_unlog(self):
    #     reponse = self.client.get(reverse('respond_issue'))
    #     self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('respond_issue'))

    # def test_url_reopen_issue_unlog(self):
    #     reponse = self.client.get(reverse('reopen_issue'))
    #     self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('reopen_issue'))

    # def test_url_view_issue_unlog(self):
    #     reponse = self.client.get(reverse('view_issue'))
    #     self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('view_issue'))

    def test_url_new_issue_unlog(self):
        reponse = self.client.get(reverse('new_issue'))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('new_issue'))
