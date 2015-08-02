# -*-coding:utf-8 -*-
"""
:module: core.tests.test_urls
:synopsis: unit testing urls for core apps

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 30/07/2015
:todo: test multilingue avec selenium
"""
from django.test import TestCase
from django.core.urlresolvers import reverse


class CoreUrlTests(TestCase):
    """
    this class define all unit tests for core

    :param TestCase: librairy of unittest
    :type TestCase: object
    :return: None
    :rtype: None
    """

    def test_home_url(self):
        """
        tests access to url home

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('home'))
        self.assertEqual(reponse.status_code, 200)
        self.assertTemplateUsed(reponse, 'core/home.html')
