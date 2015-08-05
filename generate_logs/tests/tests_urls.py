# -*-coding:utf-8 -*-
"""
:module: generate_logs.tests.tests_urls
:synopsis: unit testing urls for generate_logs app

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 04/08/2015
"""
from django.conf import settings
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from profil.models import UserLang


class GenerateLogsUrlUnlogTests(TestCase):
    """
    this class define all unit tests for generate_logs urls

    :param TestCase: librairy of unittest
    :type TestCase: object
    :return: None
    :rtype: None
    """

    def test_list_logs_url_unlog_from_home(self):
        """
        tests access to list log when nobody is logged

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('list_logs'))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('list_logs'))

    def tests_view_logs_unlog_from_home(self):
        """
        tests access to selected log type when nobody is logged

        :var reponse: response of request
        :return: None
        """
        for k, v in settings.LOGGING['handlers'].items():
            reponse = self.client.get(reverse('view_log', kwargs={'log_type': k}))
            self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('view_log', kwargs={'log_type': k}))

    def tests_view_logs_unlog_from_forum(self):
        """
        tests access to selected log type when nobody is logged

        :var reponse: response of request
        :return: None
        """
        for k, v in settings.LOGGING['handlers'].items():
            reponse = self.client.get(reverse('view_log', kwargs={'log_type': k}))
            self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('view_log', kwargs={'log_type': k}))


class GenerateLogsUrlLogTests(TestCase):
    """
    this class define all unit tests for generate_logs urls

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
        :var self.register_admin: dict for create new admin
        :var self.register_staff: dict for create new staff member
        :var new_user: instance of user contain new_user
        :var new_staff: instance of user contain new_staff
        :var new_admin: instance of user contain new_admin
        :return: None
        """
        self.client = Client()
        self.register_user = {'username': "user_test", 'email': 'user_test@tests.fr', 'password': "tests"}
        self.register_admin = {'username': "admin", 'email': 'admin@admin.fr', 'password': "admin"}
        self.register_staff = {'username': "staff", 'email': 'staff@staff.fr', 'password': "staff"}
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')
        new_admin = User.objects.create_user(**self.register_admin)
        User.objects.filter(username=self.register_admin['username']).update(is_staff=True, is_superuser=True)
        UserLang.objects.create(user=new_admin, lang='fr')
        new_staff = User.objects.create_user(**self.register_staff)
        User.objects.filter(username=self.register_staff['username']).update(is_staff=True)
        UserLang.objects.create(user=new_staff, lang='fr')

    def test_list_logs_url_log_user_from_home(self):
        """
        tests access to list log when user is log from home

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('list_logs'))
        self.assertRedirects(reponse, reverse('home'))
        self.client.logout()

    def test_list_logs_url_log_user_from_forum(self):
        """
        tests access to list log when user is log from forum page

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('list_logs'), HTTP_REFERER=reverse('forum'), follow=True)
        self.assertRedirects(reponse, reverse('forum'))
        self.client.logout()

    def test_list_logs_url_log_staff_from_home(self):
        """
        tests access to list log when staff member is log from home

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_staff['username'], password=self.register_staff['password'])
        reponse = self.client.get(reverse('list_logs'))
        self.assertRedirects(reponse, reverse('home'))
        self.client.logout()

    def test_list_logs_url_log_staff_from_forum(self):
        """
        tests access to list log when staff member is log from forum

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_staff['username'], password=self.register_staff['password'])
        reponse = self.client.get(reverse('list_logs'), HTTP_REFERER=reverse('forum'), follow=True)
        self.assertRedirects(reponse, reverse('forum'))
        self.client.logout()

    def test_list_logs_url_log_admin_from_home(self):
        """
        tests access to list log when admin is log from home

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_admin['username'], password=self.register_admin['password'])
        reponse = self.client.get(reverse('list_logs'))
        for k, v in settings.LOGGING['handlers'].items():
            if k is not 'console':
                self.assertContains(reponse, k)
            else:
                self.assertNotContains(reponse, k)
        self.assertTemplateUsed(reponse, 'logs/index.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_list_logs_url_log_admin_from_forum(self):
        """
        tests access to list log when admin is log from forum

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_admin['username'], password=self.register_admin['password'])
        reponse = self.client.get(reverse('list_logs'))
        for k, v in settings.LOGGING['handlers'].items():
            if k is not 'console':
                self.assertContains(reponse, k)
            else:
                self.assertNotContains(reponse, k)
        self.assertTemplateUsed(reponse, 'logs/index.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def tests_view_logs_log_user_from_home(self):
        """
        tests access to selected log when user is log from home

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        for k, v in settings.LOGGING['handlers'].items():
            reponse = self.client.get(reverse('view_log', kwargs={'log_type': k}))
            self.assertRedirects(reponse, reverse('home'))
        self.client.logout()

    def tests_view_logs_log_user_from_forum(self):
        """
        tests access to selected log when user is log from forum

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        for k, v in settings.LOGGING['handlers'].items():
            reponse = self.client.get(reverse('view_log', kwargs={'log_type': k}), HTTP_REFERER=reverse('forum'),
                                      follow=True)
            self.assertRedirects(reponse, reverse('forum'))
        self.client.logout()

    def tests_view_logs_log_staff_from_home(self):
        """
        tests access to selected log when staff memeber is log from home

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        for k, v in settings.LOGGING['handlers'].items():
            reponse = self.client.get(reverse('view_log', kwargs={'log_type': k}))
            self.assertRedirects(reponse, reverse('home'))
        self.client.logout()

    def tests_view_logs_log_staff_from_forum(self):
        """
        tests access to selected log when staff memeber is log from forum

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        for k, v in settings.LOGGING['handlers'].items():
            reponse = self.client.get(reverse('view_log', kwargs={'log_type': k}), HTTP_REFERER=reverse('forum'),
                                      follow=True)
            self.assertRedirects(reponse, reverse('forum'))
        self.client.logout()

    def tests_view_logs_log_admin_from_home(self):
        """
        tests access to selected log when admin is log from home

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_admin['username'], password=self.register_admin['password'])
        for k, v in settings.LOGGING['handlers'].items():
            reponse = self.client.get(reverse('view_log', kwargs={'log_type': k}), follow=True)
            if k is not 'console':
                self.assertTemplateUsed(reponse, 'logs/display_log.html')
                self.assertEqual(reponse.status_code, 200)
            else:
                self.assertRedirects(reponse, reverse('list_logs'))
        self.client.logout()

    def tests_view_logs_log_admin_from_forum(self):
        """
        tests access to selected log when admin is log from forum

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_admin['username'], password=self.register_admin['password'])
        for k, v in settings.LOGGING['handlers'].items():
            reponse = self.client.get(reverse('view_log', kwargs={'log_type': k}), HTTP_REFERER=reverse('forum'),
                                      follow=True)
            if k is not 'console':
                self.assertTemplateUsed(reponse, 'logs/display_log.html')
                self.assertEqual(reponse.status_code, 200)
            else:
                self.assertRedirects(reponse, reverse('list_logs'))
        self.client.logout()
