from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _


class RegisterTests(TestCase):
    fixtures = ["profil.json"]

    def test_register_url(self):
        reponse = self.client.get(reverse('register'))
        self.assertEqual(reponse.status_code, 200)

    def test_register(self):
        data = {
            'username': "anthony",
            'email': "chrysa@chrysa.me",
            'password': "test",
            'password_conf': "test",
        }
        reponse = self.client.post(
            reverse('register'),
            data,
            follow=True,
        )
        self.assertRedirects(
            reponse,
            reverse('home'),
            status_code=301,
            target_status_code=200,
            host=None,
            msg_prefix='',
            fetch_redirect_response=True
        )

    def test_register_user_password_error(self):
        data = {
            'username': "anthony",
            'email': "chrysa@chrysa.me",
            'password': "test",
            'password_conf': "te",
        }
        reponse = self.client.post(reverse('register'), data)
        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse.context[0]['errors']['pass'], _("error_password"))

    def test_register_user_already_exist(self):
        data = {
            'username': "chrysa",
            'email': "chrysa@chrysa.me",
            'password': "test",
            'password_conf': "test",
        }
        reponse = self.client.post(reverse('register'), data)
        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse.context[0]['errors']['user'], _("error_user_already_exist"))

    def test_register_mail_already_exist(self):
        data = {
            'username': "anthony",
            'email': "chrysa@chrysa.fr",
            'password': "test",
            'password_conf': "test",
        }
        reponse = self.client.post(reverse('register'), data)
        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse.context[0]['errors']['mail'], _("error_mail_already_exist"))


class LoginTests(TestCase):
    fixtures = ['tests.json']

    def test_login_url(self):
        reponse = self.client.get(reverse('login'))
        self.assertEqual(reponse.status_code, 200)

    def test_login(self):
        data = {
            'username': "chrysa",
            'password': "plop",
        }
        reponse = self.client.post(
            reverse('login'),
            data,
            follow=True,
        )
        self.assertRedirects(
            reponse,
            reverse('home'),
            status_code=301,
            target_status_code=200,
            host=None,
            msg_prefix='',
            fetch_redirect_response=True
        )


#     def test_login_wrong_user(self):
#         data = {
#             'username': "user_inexistant",
#             'password': "plop",
#         }
#         reponse = self.client.post(reverse('login'), data)
#         self.assertEqual(reponse.status_code, 200)
#         self.assertContains(reponse, "error_user_not_exist")

#     def test_login_wrong_password(self):
#         data = {
#             'username': "chrysa",
#             'password': "mauvais_pass",
#         }
#         reponse = self.client.post(reverse('login'), data)
#         self.assertEqual(reponse.status_code, 200)
#         self.assertContains(reponse, "error_wrong_password")


# class LogoutTests(TestCase):

#     def test_logout_user_log(self):
#         self.client.login(username='chrysa', password='plop')
#         reponse = self.client.get(reverse('logout'))
#         self.assertEqual(reponse.status_code, 200)
#         self.client.logout()

#     def test_logout(self):
#         reponse = self.client.post(reverse('logout'))
#         self.assertEqual(reponse.status_code, 301)
#         self.assertRedirects(reponse, reverse('home'))

# ajouter test de gestion de langue
