# -*-coding:utf-8 -*-
"""
:module: generate_logs.tests.tests_views_logs
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


class GenerateLogsUrlTests(TestCase):
    """
    this class define all unit tests for generate_logs view_logs

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
        :var wrong_type: wrong type long
        :return: None
        """
        self.client = Client()
        self.register_user = {'username': "user_test", 'email': 'user_test@tests.fr', 'password': "tests"}
        self.register_admin = {'username': "admin", 'email': 'admin@admin.fr', 'password': "admin"}
        self.register_staff = {'username': "staff", 'email': 'staff@staff.fr', 'password': "staff"}
        self.wrong_type = 'wrong_type'
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')
        new_admin = User.objects.create_user(**self.register_admin)
        User.objects.filter(username=self.register_admin['username']).update(is_staff=True, is_superuser=True)
        UserLang.objects.create(user=new_admin, lang='fr')
        new_staff = User.objects.create_user(**self.register_staff)
        User.objects.filter(username=self.register_staff['username']).update(is_staff=True)
        UserLang.objects.create(user=new_staff, lang='fr')

    def tests_view_logs(self):
        """
        tests display of logs

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

    def tests_view_logs_wrong_type(self):
        """
        tests display of logs with wrong type

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_admin['username'], password=self.register_admin['password'])
        reponse = self.client.get(reverse('view_log', kwargs={'log_type': self.wrong_type}), follow=True)
        self.assertRedirects(reponse, reverse('list_logs'))
        self.client.logout()
