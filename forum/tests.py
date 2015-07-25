# -*-coding:utf-8 -*-
"""
:module: forum.tests
:synopsis: unit testing for forum app

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 22/07/2015
:seealso: forum.models.ForumCat
:seealso: forum.models.ForumTopic
:seealso: profil.models.UserLang
"""
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from forum.models import ForumCat
from profil.models import UserLang


class ForumTests(TestCase):
    """
    this class define all unit test for forum

    :param TestCase: librarie of unittest
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
        :var self.register_user: dict for create new user
        :var self.create_topic: dict of datas for create topic
        :var new_user: instance of user contain new_user
        :return: None
        """
        self.client = Client()
        self.register_user = {
            'username': "user_test",
            'email': 'user_test@test.fr',
            'password': "test",
        }
        self.cat = ['cat1', 'cat2',]
        self.create_topic = {
            'Title': 'test cat',
            'Message': 'content test',
        }
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')
        for cat in self.cat:
            ForumCat(Name=cat).save()

    def test_forum_url_unlog(self):
        """
        test access to url contact not log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('forum'))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('forum'))

    def test_forum_url_log(self):
        """
        test access to url contact log status

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('forum'))
        self.assertTemplateUsed(reponse, 'forum/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_no_cat(self):
        """
        test where any categorys are define

        :var reponse: response of request
        :return: None
        """
        for cat in self.cat:
            ForumCat.objects.get(Name=cat).delete()
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('forum'))
        self.assertContains(reponse, _("no_category"))
        self.assertTemplateUsed(reponse, 'forum/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()
        for cat in self.cat:
            ForumCat(Name=cat).save()

    def create_topic_access_url(self):
        """
        test access to url for create topic

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('create_topic', kwargs={'cat': ForumCat.objects.get(slug=self.cat[0]).slug}))
        self.assertTemplateUsed(reponse, 'forum/create_topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def create_topic_access_url_unlog(self):
        """
        test access to url for create topic

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('create_topic', kwargs={'cat': ForumCat.objects.get(slug=self.cat[0]).slug}))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('forum'))

    def create_topic(self):
        """
        test create topic

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('create_topic', kwargs={'cat': ForumCat.objects.get(slug=self.cat[0]).slug}), self.create_topic, follow=True)
        self.assertTemplateUsed(reponse, 'forum/topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

# create topic sans message
# create topic sans titre
# edit topic
# access topic
# access inexistant topic
# edit inexistant topic
# response topic
# edit post
# edit inexitant post
