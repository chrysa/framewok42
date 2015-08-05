# -*-coding:utf-8 -*-
"""
:module: issues.tests.tests_urls
:synopsis: unit testing for issues urls

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 05/08/2015

:todo: tests admin acces
:todo: acces URL de reopen issue user connecte
:todo: acces URL de view conecte
:todo: acces URL de view non conecte
:todo: acces URL de new issue conecte
:todo: acces URL de new issue non conecte
:todo: tests affichage d'issue a vide

"""
from django.test import Client
from django.test import TestCase
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from profil.models import UserLang
from issues.models import Issue


class UrlIssuesTestsUnLog(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_user = {'username': "user_test", 'email': 'user_test@tests.fr', 'password': "tests"}
        self.register_admin = {'username': 'admin', 'password': 'admin'}
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')
        new_admin = User.objects.create_user(**self.register_admin)
        User.objects.filter(username=self.register_admin['username']).update(is_staff=True, is_superuser=True)
        UserLang.objects.create(user=new_admin, lang='fr')
        self.TestIssue = {'Autor': User.objects.get(username=self.register_user['username']),
                          'Assign': User.objects.get(username=self.register_admin['username']), 'Title': 'test issue',
                          'UserRequest': 'test content issue'}
        Issue(**self.TestIssue).save()
        self.issue = Issue.objects.get(Title=self.TestIssue['Title'])

    def test_url_list_issue_unlog(self):
        reponse = self.client.get(reverse('list_issue'))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('list_issue'))

    def test_url_respond_issue_unlog(self):
        reponse = self.client.get(reverse('respond_issue', kwargs={'issue': self.issue.slug}))
        self.assertRedirects(reponse,
                             reverse('login') + '?next=' + reverse('respond_issue', kwargs={'issue': self.issue.slug}))

    def test_url_reopen_issue_unlog(self):
        reponse = self.client.get(reverse('reopen_issue', kwargs={'issue': self.issue.slug}))
        self.assertRedirects(reponse,
                             reverse('login') + '?next=' + reverse('reopen_issue', kwargs={'issue': self.issue.slug}))

    def test_url_view_issue_unlog(self):
        reponse = self.client.get(reverse('view_issue', kwargs={'issue': self.issue.slug}))
        self.assertRedirects(reponse,
                             reverse('login') + '?next=' + reverse('view_issue', kwargs={'issue': self.issue.slug}))

    def test_url_new_issue_unlog(self):
        reponse = self.client.get(reverse('new_issue'))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('new_issue'))


class UrlIssuesTestsLog(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_user = {'username': "user_test", 'email': 'user_test@tests.fr', 'password': "tests"}
        self.register_admin = {'username': 'admin', 'password': 'admin'}
        self.register_staff = {'username': 'staff', 'password': 'staff'}
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')
        new_admin = User.objects.create_user(**self.register_admin)
        User.objects.filter(username=self.register_admin['username']).update(is_staff=True, is_superuser=True)
        UserLang.objects.create(user=new_admin, lang='fr')
        new_staff = User.objects.create_user(**self.register_staff)
        User.objects.filter(username=self.register_staff['username']).update(is_staff=True)
        UserLang.objects.create(user=new_staff, lang='fr')
        self.TestIssue = {'Autor': User.objects.get(username=self.register_user['username']),
                          'Assign': User.objects.get(username=self.register_admin['username']), 'Title': 'test issue',
                          'UserRequest': 'test content issue'}
        Issue(**self.TestIssue).save()
        self.issue = Issue.objects.get(Title=self.TestIssue['Title'])

    def test_url_list_issue_user_log(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('list_issue'))
        self.assertContains(reponse, _("list_issue_user"))
        self.assertTemplateUsed(reponse, 'issues/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_url_list_issue_admin_log(self):
        self.client.login(username=self.register_admin['username'], password=self.register_admin['password'])
        reponse = self.client.get(reverse('list_issue'))
        self.assertContains(reponse, _("list_issue_admin"))
        self.assertTemplateUsed(reponse, 'issues/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_url_list_issue_staff_log(self):
        self.client.login(username=self.register_staff['username'], password=self.register_staff['password'])
        reponse = self.client.get(reverse('list_issue'))
        self.assertContains(reponse, _("list_issue_admin"))
        self.assertTemplateUsed(reponse, 'issues/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_url_respond_issue_user_log(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('respond_issue', kwargs={'issue': self.issue.slug}), follow=True)
        self.assertRedirects(reponse, reverse('view_issue', kwargs={'issue': self.issue.slug}), status_code=301,
                             target_status_code=200, fetch_redirect_response=True)
        self.client.logout()

    def test_url_respond_issue_admin_log(self):
        self.client.login(username=self.register_admin['username'], password=self.register_admin['password'])
        reponse = self.client.get(reverse('respond_issue', kwargs={'issue': self.issue.slug}), follow=True)
        self.assertContains(reponse, _("list_issue_admin"))
        self.assertTemplateUsed(reponse, 'issues/issue_admin_response.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_url_respond_issue_staff_log(self):
        self.client.login(username=self.register_staff['username'], password=self.register_staff['password'])
        reponse = self.client.get(reverse('respond_issue', kwargs={'issue': self.issue.slug}), follow=True)
        self.assertContains(reponse, _("list_issue_admin"))
        self.assertTemplateUsed(reponse, 'issues/issue_admin_response.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_url_reopen_issue_admin_log(self):
        self.client.login(username=self.register_admin['username'], password=self.register_admin['password'])
        reponse = self.client.get(reverse('reopen_issue', kwargs={'issue': self.issue.slug}))
        self.assertRedirects(reponse,
                             reverse('login') + '?next=' + reverse('reopen_issue', kwargs={'issue': self.issue.slug}))
        self.client.logout()

# respond invalid issue
# view invalid issue
# reopen issue
# reopen invalid issue
# reopen issue wrong user
