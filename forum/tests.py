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
        self.assertRedirects(reponse,
                             reverse('login') + '?next=' + reverse('create_topic', kwargs={'cat': self.cat_slug}))

    def test_create_topic(self):
        """
        test create topic

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('create_topic', kwargs={'cat': ForumCat.objects.get(slug=self.cat_slug)}),
                                   self.create_topic, follow=True)
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
        reponse = self.client.post(reverse('create_topic', kwargs={'cat': ForumCat.objects.get(slug=self.cat_slug)}),
                                   create_topic, follow=True)
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
        """
        test access to topic

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
        test access to topic unlog

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.post(reverse('topic_cat', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}),
                                   follow=True)
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('topic_cat', kwargs={'cat': self.cat_slug,
                                                                                                 'topic': self.topic_slug}))

    def test_acces_to_topic_with_inexisting_cat(self):
        """
        test access to topic with wrong cat

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('topic_cat', kwargs={'cat': self.inexisting_cat, 'topic': self.topic_slug}),
                                   follow=True)
        self.assertContains(reponse, self.cat[0])
        self.assertTemplateUsed(reponse, 'forum/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_acces_to_topic_with_inexisting_topic(self):
        """
        test access to a wrong topic

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('topic_cat', kwargs={'cat': self.cat_slug, 'topic': self.inexisting_topic}),
                                   follow=True)
        self.assertContains(reponse, self.cat[0])
        self.assertContains(reponse, self.ref_topic['Title'])
        self.assertTemplateUsed(reponse, 'forum/cat.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_acces_to_topic_with_inexisting_topic_cat_and_topic(self):
        """
        test access to topic with wrong cat and a wrong topic

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(
            reverse('topic_cat', kwargs={'cat': self.inexisting_cat, 'topic': self.inexisting_topic}), follow=True)
        self.assertContains(reponse, self.cat[0])
        self.assertTemplateUsed(reponse, 'forum/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_response_topic(self):
        """
        test to response at a topic

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
        test to edit at a topic unlog

        :var reponse: response of request
        :return: None
        """
        reponse = self.client.post(reverse('edit_topic', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}),
                                   self.edit_topic, follow=True)
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('edit_topic', kwargs={'cat': self.cat_slug,
                                                                                                  'topic': self.topic_slug}))

    def test_edit_topic_title_message(self):
        """
        test to edit at a topic

        :var reponse: response of request
        :return: None
        """
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('edit_topic', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}),
                                   self.edit_topic, follow=True)
        self.assertContains(reponse, self.edit_topic['Message'])
        self.assertContains(reponse, self.edit_topic['Title'])
        self.assertTemplateUsed(reponse, 'forum/topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_edit_topic_title(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        dump_title = self.edit_topic['Title']
        self.edit_topic['Title'] = self.ref_topic['Title']
        reponse = self.client.post(reverse('edit_topic', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}),
                                   self.edit_topic, follow=True)
        self.assertContains(reponse, self.ref_topic['Title'])
        self.assertContains(reponse, self.edit_topic['Message'])
        self.assertTemplateUsed(reponse, 'forum/topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.edit_topic['Title'] = dump_title
        self.client.logout()

    def test_edit_topic_message(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        dump_mess = self.edit_topic['Message']
        self.edit_topic['Message'] = self.ref_topic['Message']
        reponse = self.client.post(reverse('edit_topic', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}),
                                   self.edit_topic, follow=True)
        self.assertContains(reponse, self.edit_topic['Title'])
        self.assertContains(reponse, self.ref_topic['Message'])
        self.assertTemplateUsed(reponse, 'forum/topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.edit_topic['Message'] = dump_mess
        self.client.logout()

    def test_edit_topic_blank_title(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        dump_title = self.edit_topic['Title']
        self.edit_topic['Title'] = ''
        reponse = self.client.post(reverse('edit_topic', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}),
                                   self.edit_topic, follow=True)
        self.assertContains(reponse, self.ref_topic['Title'])
        self.assertContains(reponse, self.ref_topic['Message'])
        self.assertTemplateUsed(reponse, 'forum/create_topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.edit_topic['Title'] = dump_title
        self.client.logout()

    def test_edit_topic_blank_message(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        dump_mess = self.edit_topic['Message']
        self.edit_topic['Message'] = ''
        reponse = self.client.post(reverse('edit_topic', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug}),
                                   self.edit_topic, follow=True)
        self.assertContains(reponse, self.ref_topic['Title'])
        self.assertContains(reponse, self.ref_topic['Message'])
        self.assertTemplateUsed(reponse, 'forum/create_topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.edit_topic['Message'] = dump_mess
        self.client.logout()

    def test_edit_inexisting_cat(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('edit_topic', kwargs={'cat': self.inexisting_cat, 'topic': self.topic_slug}),
                                   self.edit_topic, follow=True)
        self.assertContains(reponse, self.ref_topic['Title'])
        self.assertContains(reponse, self.ref_topic['Message'])
        self.assertTemplateUsed(reponse, 'forum/create_topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_edit_inexisting_topic(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(reverse('edit_topic', kwargs={'cat': self.cat_slug, 'topic': self.inexisting_topic}),
                                   self.edit_topic, follow=True)
        self.assertTemplateUsed(reponse, 'forum/cat.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_edit_inexisting_cat_topic(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(
            reverse('edit_topic', kwargs={'cat': self.inexisting_cat, 'topic': self.inexisting_topic}), self.edit_topic,
            follow=True)
        self.assertContains(reponse, self.cat[0])
        self.assertTemplateUsed(reponse, 'forum/home.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def test_edit_post_unlog(self):
        post = ForumPost.objects.get(Message=self.ref_response['Message'])
        reponse = self.client.post(
            reverse('edit_post', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug, 'post': post.pk}),
            self.edit_post, follow=True)
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('edit_post', kwargs={'cat': self.cat_slug,
                                                                                                 'topic': self.topic_slug,
                                                                                                 'post': post.pk}))

    def test_edit_post(self):
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

    def test_edit_post_blank(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.post(
            reverse('edit_post', kwargs={'cat': self.cat_slug, 'topic': self.topic_slug, 'post': self.inexisting_post}),
            self.ref_response, follow=True)
        self.assertContains(reponse, self.ref_response['Message'])
        self.assertTemplateUsed(reponse, 'forum/topic.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()
