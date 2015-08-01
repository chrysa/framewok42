# -*-coding:utf-8 -*-
"""
:module: forum.tests.tests_posts
:synopsis: unit testing posts for forum app

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 30/07/2015
:seealso: forum.models.ForumCat
:seealso: forum.models.ForumTopic
:seealso: forum.models.ForumPost
:seealso: profil.models.UserLang
:todo: clean unit test
:todo: internationalisation
"""
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from forum.models import ForumCat
from forum.models import ForumTopic
from forum.models import ForumPost
from profil.models import UserLang


class ForumTests(TestCase):
    """
    this class define all unit test for forum

    :param TestCase: librairy of unittest
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
        self.cat = ['cat1', 'cat2', ]
        self.ref_topic = {
            'Title': 'ref topic',
            'Message': 'content test',
        }
        self.create_topic = {
            'Title': 'test topic',
            'Message': 'content test',
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
        ForumPost(
            TopicParent=ForumTopic.objects.get(
                slug=self.topic_slug
            ),
            Message=self.ref_response['Message'],
            Autor=User.objects.get(username=self.register_user['username']),
        ).save()

    def test_edit_post_unlog(self):
        """
        test to edit a post with unlog user

        :var reponse: response of request
        :return: None
        """
        post = ForumPost.objects.get(Message=self.ref_response['Message'])
        reponse = self.client.post(
            reverse('edit_post', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug, 'post': post.pk}),
            self.edit_post, follow=True)
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('edit_post', kwargs={'cat': self.cat_slug,
                                                                                                 'topic': self.topic_slug,
                                                                                                 'post': post.pk}))

    def test_edit_post(self):
        """
        test to edit a post

        :var reponse: response of request
        :return: None
        """
        post = ForumPost.objects.get(Message=self.ref_response['Message'])
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(
            reverse('edit_post', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug, 'post': post.pk}),
            self.edit_post, follow=True)
        self.assertContains(reponse, self.edit_post['Message'])
        self.assertTemplateUsed(reponse, 'forum/topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_edit_post_blank(self):
        """
        test to edit a post with blank message

        :var reponse: response of request
        :return: None
        """
        post = ForumPost.objects.get(Message=self.ref_response['Message'])
        dump_mess = self.ref_response['Message']
        self.ref_response['Message'] = ''
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(
            reverse('edit_post', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug, 'post': post.pk}),
            self.ref_response, follow=True)
        self.assertContains(reponse, _('post_must_contain_message'))
        self.assertContains(reponse, dump_mess)
        self.assertTemplateUsed(reponse, 'forum/edit_post.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()
        self.ref_response['Message'] = dump_mess

    def test_edit_inexistant_post(self):
        """
        test to edit a wrong topic

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(
            reverse('edit_post', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug, 'post': self.inexisting_post}),
            self.ref_response, follow=True)
        self.assertContains(reponse, self.ref_response['Message'])
        self.assertTemplateUsed(reponse, 'forum/topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()
