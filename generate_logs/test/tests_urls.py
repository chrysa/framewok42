# -*-coding:utf-8 -*-
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from profil.models import UserLang


class LogsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_user = {
            'username': "user_test",
            'email': 'user_test@test.fr',
            'password': "test",
        }
        self.admin_datas = {
            'username': 'admin',
            'password': 'admin',
        }
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')
        User.objects.create_user(**self.admin_datas)
        User.objects.filter(username=self.admin_datas['username']).update(is_staff=True, is_superuser=True)

    def test_list_logs_url(self):
        reponse = self.client.get(reverse('list_logs'))
        self.assertEqual(reponse.status_code, 200)
        self.assertTemplateUsed(reponse, 'logs/index.html')

#acces url list not log
#acces url list user log
#acces url list admin log
#acces url spe not log
#acces url spe user log
#acces url spe admin log
    def test_co_admin(self):
        reponse = self.client.post(reverse('admin:index'), self.admin_datas, follow=True)

#test aces par type de categorie
#test aces par categorie inexistante