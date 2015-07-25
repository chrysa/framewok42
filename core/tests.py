# -*-coding:utf-8 -*-
"""
:module: core.tests
:synopsis: unit testing for core apps

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 22/07/2015
"""
from django.test import TestCase
from django.core.urlresolvers import reverse


class CoreUrlTests(TestCase):

    """
    this class define all unit test for core

    :param TestCase: librarie of unittest
    :type TestCase: object
    :return: None
    :rtype: None
    """

    def test_home_url(self):
        """
        test access to url home

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('home'))
        self.assertEqual(reponse.status_code, 200)
        self.assertTemplateUsed(reponse, 'core/home.html')
