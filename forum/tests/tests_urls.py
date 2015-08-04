# -*-coding:utf-8 -*-
"""
:module: forum.tests.tests_urls
:synopsis: unit testing urls for forum app

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 30/07/2015
:seealso: forum.models.ForumCat
:seealso: forum.models.ForumTopic
:seealso: forum.models.ForumPost
:seealso: profil.models.UserLang
:todo: tests acces to topic
:todo: tests acces to inexisting topic
:todo: clean unit tests
"""
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from forum.models import ForumCat
from forum.models import ForumTopic
from forum.models import ForumPost
from profil.models import UserLang


class ForumTests(TestCase):
    """
    this class define all unit tests for forum

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
        :var self.create_topic: dict of datas for create topic
        :var new_user: instance of user contain new_user
        :return: None
        """
        self.client = Client()
        self.register_user = {
            'username': "user_test",
            'email': 'user_test@tests.fr',
            'password': "tests",
        }
        self.cat = ['cat1', 'cat2', ]
        self.ref_topic = {
            'Title': 'ref topic',
            'Message': 'content tests',
        }
        self.create_topic = {
            'Title': 'tests topic',
            'Message': 'content tests',
        }
        self.ref_response = {
            'Message': 'ref_reponse',
        }
        self.test_response = {
            'Message': 'test_reponse',
        }
        self.edit_topic = {
            'Title': 'edit topic title',
            'Message': 'edit topic message',
        }
        self.edit_post = {
            'Message': 'edit post',
        }
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')
        for cat in self.cat:
            ForumCat(Name=cat).save()
        ForumTopic(
            CatParent=ForumCat.objects.get(Name=self.cat[0]),
            Title=self.ref_topic['Title'],
            Autor=User.objects.get(username=self.register_user['username']),
            Message=self.ref_topic['Message']
        ).save()
        self.inexisting_cat = 'inexisting-cat'
        self.inexisting_topic = 'inexisting-topic'
        self.inexisting_post = '100'
        self.cat_slug = ForumCat.objects.get(Name=self.cat[0]).slug
        self.topic_slug = ForumTopic.objects.get(CatParent=ForumCat.objects.get(Name=self.cat[0])).slug
        ForumPost(TopicParent=ForumTopic.objects.get(slug=self.topic_slug), Message=self.ref_response['Message'],
                  Autor=User.objects.get(username=self.register_user['username'])).save()

    def test_forum_url_unlog(self):
        """
        tests access to url contact not log status

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('forum'))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('forum'))

    def test_forum_url_log(self):
        """
        tests access to url contact log status

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('forum'))
        self.assertTemplateUsed(reponse, 'forum/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_acces_existing_cat(self):
        """
        tests access to existing category

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('cat', kwargs={'cat': self.cat[0]}))
        self.assertContains(reponse, self.cat[0])
        self.assertContains(reponse, self.ref_topic['Title'])
        self.assertTemplateUsed(reponse, 'forum/cat.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_acces_not_existing_cat(self):
        """
        tests access to category who aren't define

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('cat', kwargs={'cat': self.inexisting_cat}))
        self.assertContains(reponse, self.cat[0])
        self.assertTemplateUsed(reponse, 'forum/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_create_topic_access_url(self):
        """
        tests access to url for create topic if user log

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('create_topic', kwargs={'cat': self.cat_slug}))
        self.assertTemplateUsed(reponse, 'forum/create_topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_create_topic_access_url_unlog(self):
        """
        tests access to url for create topic if any user log

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('create_topic', kwargs={'cat': ForumCat.objects.get(slug=self.cat[0]).slug}))
        self.assertRedirects(reponse,
                             reverse('login') + '?next=' + reverse('create_topic', kwargs={'cat': self.cat_slug}))

    def test_acces_to_topic(self):
        """
        tests access to topic

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('topic_cat', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}),
                                   follow=True)
        self.assertContains(reponse, self.ref_topic['Title'])
        self.assertContains(reponse, self.ref_topic['Message'])
        self.assertTemplateUsed(reponse, 'forum/topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_acces_to_topic_unlog(self):
        """
        tests access to topic unlog

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.post(reverse('topic_cat', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}),
                                   follow=True)
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('topic_cat', kwargs={'cat': self.cat_slug,
                                                                                                 'topic': self.topic_slug}))

    def test_response_topic(self):
        """
        tests to response at a topic

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('send_reply', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}),
                                   self.test_response, HTTP_REFERER=reverse('topic_cat', kwargs={'cat': self.cat_slug,
                                                                                                 'topic': self.topic_slug}),
                                   follow=True)
        self.assertContains(reponse, self.test_response['Message'])
        self.assertTemplateUsed(reponse, 'forum/topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_edit_topic_unlog(self):
        """
        tests to edit a topic when no user log

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.post(reverse('edit_topic', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}),
                                   self.edit_topic, follow=True)
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('edit_topic', kwargs={'cat': self.cat_slug,
                                                                                                  'topic': self.topic_slug}))
