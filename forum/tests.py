# -*-coding:utf-8 -*-
"""
:module: forum.tests
:synopsis: unit testing for forum app

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 22/07/2015
:seealso: forum.models.ForumCat
:seealso: forum.models.ForumTopic
:seealso: forum.models.ForumPost
:seealso: profil.models.UserLang
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
        ForumPost(
            TopicParent=ForumTopic.objects.get(
                CatParent=ForumCat.objects.get(Name=self.cat[0]),
                Autor=User.objects.get(username=self.register_user['username']),
                Message=['Message']
            )
        ).save()
        self.cat_slug = ForumCat.objects.get(Name=self.cat[0]).slug
        self.topic_slug = ForumTopic.objects.get(CatParent=ForumCat.objects.get(Name=self.cat[0])).slug
        self.inexisting_cat = 'inexisting_cat'
        self.inexisting_topic = 'inexisting_topic'


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

    def test_without_cat(self):
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

    def test_with_cat(self):
        """
        test where categorys are define

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('forum'))
        self.assertNotContains(reponse, _("no_category"))
        self.assertContains(reponse, self.cat[0])
        self.assertTemplateUsed(reponse, 'forum/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_acces_existing_cat(self):
        """
        test access to existing category

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
        test access to category who aren't define

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
        test access to url for create topic if user log

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
        test access to url for create topic if any user log

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.get(reverse('create_topic', kwargs={'cat': ForumCat.objects.get(slug=self.cat[0]).slug}))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('create_topic', kwargs={'cat': self.cat_slug}))

    def test_create_topic(self):
        """
        test create topic

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('create_topic', kwargs={'cat': ForumCat.objects.get(slug=self.cat_slug)}), self.create_topic, follow=True)
        self.assertTemplateUsed(reponse, 'forum/topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_create_topic_without_title(self):
        """
        test create topic without title

        :var reponse: response of request
        :return: None
        """
        create_topic = self.create_topic
        create_topic['Title'] = ''
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('create_topic', kwargs={'cat': ForumCat.objects.get(slug=self.cat_slug)}), create_topic, follow=True)
        self.assertContains(reponse, _("topic_must_contain_title"))
        self.assertTemplateUsed(reponse, 'forum/create_topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_create_topic_without_message(self):
        """
        test create topic without message

        :var reponse: response of request
        :return: None
        """
        create_topic = self.create_topic
        create_topic['Message'] = ''
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('create_topic', kwargs={'cat': self.cat_slug}), create_topic, follow=True)
        self.assertContains(reponse, _("topic_must_contain_message"))
        self.assertTemplateUsed(reponse, 'forum/create_topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_acces_to_topic(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('topic_cat', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}), follow=True)
        self.assertContains(reponse, self.ref_topic['Title'])
        self.assertContains(reponse, self.ref_topic['Message'])
        self.assertTemplateUsed(reponse, 'forum/topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_acces_to_topic_with_inexisting_topic_cat(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('topic_cat', kwargs={'cat': self.inexisting_cat, 'topic': self.topic_slug}), follow=True)
        self.assertContains(reponse, self.cat[0])
        self.assertTemplateUsed(reponse, 'forum/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_acces_to_topic_with_inexisting_topic(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('topic_cat', kwargs={'cat': self.cat_slug, 'topic': self.inexisting_topic}), follow=True)
        self.assertContains(reponse, self.cat[0])
        self.assertContains(reponse, self.ref_topic['Title'])
        self.assertTemplateUsed(reponse, 'forum/cat.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_acces_to_topic_with_inexisting_topic_cat_and_topic(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('topic_cat', kwargs={'cat': self.inexisting_cat, 'topic': self.inexisting_topic}), follow=True)
        self.assertContains(reponse, self.cat[0])
        self.assertTemplateUsed(reponse, 'forum/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_response_topic(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('send_reply', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}), self.test_response, follow=True)
        print(reponse.content)
        self.assertContains(reponse, self.test_response['message'])
        self.assertTemplateUsed(reponse, 'forum/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

# edit topic
# edit post
