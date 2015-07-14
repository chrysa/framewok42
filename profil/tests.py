from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from profil.models import UserLang


class RegisterTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_user = {
            'username': "user_test",
            'email': "user_test@test.fr",
            'password': "test",
            'password_conf': "test",
        }
        self.unittest_en = {
            'username': 'unittest_en',
            'email': 'unittest_en@unittest.fr',
            'password': 'unittest'
        }
        self.unittest_fr = {
            'username': 'unittest_fr',
            'email': 'unittest_fr@unittest.fr',
            'password': 'unittest'
        }
        unittest_en = User.objects.create_user(self.unittest_en)
        unittest_fr = User.objects.create_user(self.unittest_fr)
        UserLang.objects.create(user=unittest_en, lang='en')
        UserLang.objects.create(user=unittest_fr, lang='fr')

    def test_register_url(self):
        reponse = self.client.get(reverse('register'))
        self.assertEqual(reponse.status_code, 200)

    def register_anonymous(self):
        response = self.client.post(reverse('register'), follow=True)
        self.assertRedirects(response, reverse('home'))

    # def test_acces_register_when_login_from_home(self):
    #     self.client.login(username=self.unittest_fr['username'], password=self.unittest_fr['password'])
    #     reponse = self.client.get(
    #         reverse('register'),
    #         follow=True
    #     )
    #     print(reponse.redirect_chain)
    #     self.assertRedirects(
    #         reponse,
    #         reverse('home'),
    #         status_code=301,
    #         target_status_code=200,
    #         host=None,
    #         msg_prefix='',
    #         fetch_redirect_response=True
    #     )
    #     self.client.logout()

#     def test_acces_register_when_login_from_anywhere(self):
#         self.client.login(username=self.unittest_fr['username'], password=self.unittest_fr['password'])
#         reponse = self.client.get(
#             reverse('register') + '?next=' + reverse('contact'),
#             follow=True
#         )
#         self.assertRedirects(
#             reponse,
#             reverse('contact'),
#             status_code=301,
#             target_status_code=200,
#             host=None,
#             msg_prefix='',
#             fetch_redirect_response=True
#         )
#         self.client.logout()

    def test_register_with_blank_datas(self):
        reponse = self.client.post(
            reverse('register'),
            {},
            follow=True,
        )
        self.assertFormError(reponse, 'form', 'username', 'Ce champ est obligatoire.')
        self.assertFormError(reponse, 'form', 'email', 'Ce champ est obligatoire')
        self.assertFormError(reponse, 'form', 'password', 'Ce champ est obligatoire')
        self.assertFormError(reponse, 'form', 'password_conf', 'Ce champ est obligatoire')

    def test_register_with_wrong_mail_format(self):
        user_test = self.register_user
        user_test['email'] = 'plop@sda'
        reponse = self.client.post(
            reverse('register'),
            user_test,
            follow=True,
        )
        self.assertFormError(reponse, 'form', 'email', 'Saisissez une adresse de courriel valide.')


#     def test_register_from_home(self):
#         reponse = self.client.post(
#             reverse('register'),
#             self.register_user,
#             follow=True,
#         )
#         self.assertRedirects(
#             reponse,
#             reverse('home'),
#             status_code=301,
#             target_status_code=200,
#             host=None,
#             msg_prefix='',
#             fetch_redirect_response=True
#         )
#
#     def test_register_from_anywhere(self):
#         data = self.register_user
#         data['password_conf'] = 'error'
#         reponse = self.client.post(
#             reverse('register') + '?next=' + reverse('contact'),
#             data,
#             follow=True,
#         )
#         self.assertRedirects(
#             reponse,
#             reverse('contact'),
#             status_code=301,
#             target_status_code=200,
#             host=None,
#             msg_prefix='',
#             fetch_redirect_response=True
#         )
#
#     def test_register_user_password_error(self):
#         data = self.unittest_fr
#         reponse = self.client.post(reverse('register'), data)
#         self.assertEqual(reponse.status_code, 200)
#         self.assertEqual(
#             reponse.context[0]['errors']['pass'], _("error_password"))
#
#     def test_register_user_already_exist(self):
#         data = {
#             'username': "chrysa",
#             'email': "chrysa@chrysa.me",
#             'password': "test",
#             'password_conf': "test",
#         }
#         reponse = self.client.post(reverse('register'), data)
#         self.assertEqual(reponse.status_code, 200)
#         self.assertEqual(
#             reponse.context[0]['errors']['user'],
#             _("error_user_already_exist")
#         )
#
#     def test_register_mail_already_exist(self):
#         data = {
#             'username': "anthony",
#             'email': "chrysa@chrysa.fr",
#             'password': "test",
#             'password_conf': "test",
#         }
#         reponse = self.client.post(reverse('register'), data)
#         self.assertEqual(reponse.status_code, 200)
#         self.assertEqual(
#             reponse.context[0]['errors']['mail'],
#             _("error_mail_already_exist")
#         )
#
#
# class LoginTests(TestCase):
#     fixtures = ['profil.json']
#
#     def test_login_url(self):
#         reponse = self.client.get(reverse('login'))
#         self.assertEqual(reponse.status_code, 200)
#
#     def test_login_home(self):
#         data = {
#             'username': "chrysa",
#             'password': "plop",
#         }
#         reponse = self.client.post(
#             reverse('login'),
#             data,
#             follow=True,
#         )
#         self.assertRedirects(
#             reponse,
#             reverse('home'),
#             status_code=301,
#             target_status_code=200,
#             host=None,
#             msg_prefix='',
#             fetch_redirect_response=True
#         )
#
#     def test_login_contact(self):
#         data = {
#             'username': "chrysa",
#             'password': "plop",
#         }
#         reponse = self.client.post(
#             reverse('login'),
#             data,
#             follow=True,
#             HTTP_REFERER=reverse('contact'),
#         )
#         self.assertRedirects(
#             reponse,
#             reverse('contact'),
#             status_code=301,
#             target_status_code=200,
#             host=None,
#             msg_prefix='',
#             fetch_redirect_response=True
#         )
#
#     def test_login_forum(self):
#         data = {
#             'username': "chrysa",
#             'password': "plop",
#         }
#         reponse = self.client.post(
#             reverse('login'),
#             data,
#             follow=True,
#             HTTP_REFERER=reverse('forum'),
#         )
#         self.assertRedirects(
#             reponse,
#             reverse('forum'),
#             status_code=301,
#             target_status_code=200,
#             host=None,
#             msg_prefix='',
#             fetch_redirect_response=True
#         )
#
#     def test_login_wrong_user(self):
#         data = {
#             'username': "user_inexistant",
#             'password': "plop",
#         }
#         reponse = self.client.post(reverse('login'), data)
#         self.assertEqual(reponse.status_code, 200)
#         self.assertContains(reponse, "error_user_not_exist")
#
#     def test_login_wrong_password(self):
#         data = {
#             'username': "chrysa",
#             'password': "mauvais_pass",
#         }
#         reponse = self.client.post(reverse('login'), data)
#         self.assertEqual(reponse.status_code, 200)
#         self.assertContains(reponse, "error_wrong_password")
#
#
# class LogoutTests(TestCase):
#
#     def test_logout_user_log(self):
#         self.client.login(username='chrysa', password='plop')
#         reponse = self.client.get(reverse('logout'))
#         self.assertEqual(reponse.status_code, 200)
#         self.client.logout()
#
#     def test_logout(self):
#         reponse = self.client.post(reverse('logout'))
#         self.assertEqual(reponse.status_code, 301)
#         self.assertRedirects(reponse, reverse('home'))

# ajouter test de gestion de langue
