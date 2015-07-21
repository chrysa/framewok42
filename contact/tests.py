# -*-coding:utf-8 -*-
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from profil.models import UserLang


class ContactTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_user = {
            'username': "user_test",
            'email': 'user_test@test.fr',
            'password': "test",
        }

        unittest_fr = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=unittest_fr, lang='fr')

    def test_contact_url_unlog(self):
        reponse = self.client.get(reverse('contact'))
        self.assertContains(reponse, _("mail_adress"))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def test_contact_url_log(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('contact'))
        self.assertNotContains(reponse, _("mail_adress"))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def send_contact_unlog(self):
        reponse = self.client.get(reverse('contact'),
                                  {'email': 'test@test.fr', 'subject': 'mail unit test', 'message': 'message de test'})
        self.assertContains(reponse, _("contact_success"))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def send_contact_log(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('contact'), {'subject': 'mail unit test', 'message': 'message de test'})
        self.assertContains(reponse, _("contact_success"))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()

    def send_contact_unlog_vide(self):
        reponse = self.client.get(reverse('contact'), {})
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertContains(reponse, _('contact_must_contain_message'))
        self.assertContains(reponse, _('contact_must_contain_email'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)

    def send_contact_log_vide(self):
        self.client.login(username=self.register_user['username'], password=self.register_user['password'])
        reponse = self.client.get(reverse('contact'), {})
        self.assertContains(reponse, _('contact_must_contain_subject'))
        self.assertContains(reponse, _('contact_must_contain_message'))
        self.assertTemplateUsed(reponse, 'contact/contact.html')
        self.assertEqual(reponse.status_code, 200)
        self.client.logout()
