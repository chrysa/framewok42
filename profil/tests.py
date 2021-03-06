"""
:todo: internationalisation
:todo: logout staff et admin
"""
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
            'email': 'user_test@tests.fr',
            'password': "tests",
            'password_conf': "tests"
        }
        self.unittest_fr = {
            'username': 'unittest_fr',
            'email': 'unittest_fr@unittest.fr',
            'password': 'unittest'
        }
        unittest_fr = User.objects.create_user(**self.unittest_fr)
        UserLang.objects.create(user=unittest_fr, lang='fr')

    def test_register_url(self):
        reponse = self.client.get(reverse('register'))
        self.assertEqual(reponse.status_code, 200)
        self.assertTemplateUsed(reponse, 'profil/register.html')

    def test_register_with_blank_datas(self):
        reponse = self.client.post(reverse('register'), {}, follow=True)
        self.assertEqual(reponse.status_code, 200)
        self.assertFormError(reponse, 'form', 'username', 'Ce champ est obligatoire.')
        self.assertFormError(reponse, 'form', 'email', 'Ce champ est obligatoire.')
        self.assertFormError(reponse, 'form', 'password', 'Ce champ est obligatoire.')
        self.assertFormError(reponse, 'form', 'password_conf', 'Ce champ est obligatoire.')

    def test_register_user_password_error(self):
        data = self.unittest_fr
        data['password_conf'] = "error"
        reponse = self.client.post(reverse('register'), data, follow=True)
        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse.context[0]['errors']['pass'], _("error_wrong_password"))

    def test_register_user_already_exist(self):
        data = self.unittest_fr
        data['email'] = 'plop@unittest.fr'
        data['password_conf'] = self.unittest_fr['password']
        reponse = self.client.post(reverse('register'), data)
        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(
            reponse.context[0]['errors']['user'], _("error_user_already_exist"))

    def test_register_mail_already_exist(self):
        data = self.unittest_fr
        data['username'] = "plop"
        data['password_conf'] = self.unittest_fr['password']
        reponse = self.client.post(reverse('register'), data)
        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(
            reponse.context[0]['errors']['mail'], _("error_mail_already_exist"))

    def test_register_from_home(self):
        reponse = self.client.post(reverse('register'), self.register_user, follow=True)
        self.assertRedirects(reponse, reverse('home'), status_code=301, target_status_code=200, host=None,
                             msg_prefix='', fetch_redirect_response=True)

    def test_register_from_anywhere(self):
        reponse = self.client.post(reverse('register') + '?next=' + reverse('contact'), self.register_user,
                                   follow=True, )
        self.assertRedirects(reponse, reverse('contact'), status_code=301,
                             target_status_code=200, host=None, msg_prefix='', fetch_redirect_response=True)

    def test_acces_register_when_login_from_home(self):
        self.client.login(
            username=self.unittest_fr['username'], password=self.unittest_fr['password'])
        reponse = self.client.get(reverse('register'), follow=True)
        self.assertRedirects(reponse, reverse('home'), status_code=301, target_status_code=200, host=None,
                             msg_prefix='', fetch_redirect_response=True)
        self.client.logout()

    def test_acces_register_when_login_from_anywhere(self):
        self.client.login(username=self.unittest_fr['username'], password=self.unittest_fr['password'])
        reponse = self.client.get(reverse('register'), HTTP_REFERER=reverse('contact'), follow=True)
        self.assertRedirects(reponse, reverse('contact'), status_code=301, target_status_code=200, host=None,
                             msg_prefix='', fetch_redirect_response=True)
        self.client.logout()


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = {
            'username': "admin",
            'email': "admin@admin.fr",
            'password': "admin",
        }
        self.register_user = {
            'username': "user_test",
            'email': 'user_test@tests.fr',
            'password': "tests",
        }
        self.staff = {
            'username': "staff",
            'email': "ataff@staff.fr",
            'password': "staff",
        }
        self.log_user = {
            'username': self.register_user['username'],
            'password': self.register_user['password'],
        }
        unittest_fr = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=unittest_fr, lang='fr')
        User.objects.create_superuser(**self.admin)
        staff = User.objects.create(
            username=self.staff['username'], email=self.staff['email'], is_staff=True)
        staff.set_password(self.staff['password'])
        staff.save()

    def test_login_select_url(self):
        reponse = self.client.get(reverse('login'))
        self.assertEqual(reponse.status_code, 200)

    def test_login_local_url(self):
        reponse = self.client.get(reverse('login_classic'))
        self.assertEqual(reponse.status_code, 200)

    def test_login_home(self):
        reponse = self.client.post(reverse('login_classic'), {'username': self.register_user['username'],
                                                           'password': self.register_user['password']}, follow=True)
        self.assertRedirects(reponse, reverse(
            'home'), status_code=301, target_status_code=200, host=None, msg_prefix='', fetch_redirect_response=True)

    def test_login_contact(self):
        reponse = self.client.post(reverse('login_classic') + '?next=' + reverse('contact'), self.log_user, follow=True)
        self.assertRedirects(reponse, reverse('contact'), status_code=301, target_status_code=200, host=None,
                             msg_prefix='', fetch_redirect_response=True)

    def test_login_forum(self):
        reponse = self.client.post(reverse('login_classic') + '?next=' + reverse('forum'), self.log_user, follow=True)
        self.assertRedirects(reponse, reverse('forum'), status_code=301, target_status_code=200, host=None,
                             msg_prefix='', fetch_redirect_response=True)

    def test_login_wrong_user(self):
        data = self.log_user
        data['username'] = "wrong_user"
        reponse = self.client.post(reverse('login_classic'), data)
        self.assertContains(reponse, _("error_user_not_exist"))
        self.assertEqual(reponse.status_code, 200)

    def test_login_wrong_password(self):
        data = self.log_user
        data['password'] = "wrong_password"
        reponse = self.client.post(reverse('login_classic'), data)
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, _("error_wrong_password"))


class LogoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_user = {
            'username': "user_test",
            'email': 'user_test@tests.fr',
            'password': "tests",
        }
        self.log_user = {
            'username': self.register_user['username'],
            'password': self.register_user['password'],
        }
        unittest_fr = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=unittest_fr, lang='fr')

    def test_logout_user(self):
        self.client.login(username=self.log_user['username'], password=self.log_user['password'])
        reponse = self.client.get(reverse('logout'))
        self.assertEqual(reponse.status_code, 301)
        self.client.logout()

    def test_logout_url_unlog(self):
        """
        tests access to url contact not log status

        :var reponse: response of request
        :todo: see how to remove next when referer is logout
        :return: None
        """
        reponse = self.client.get(reverse('logout'))
        self.assertRedirects(reponse, reverse('login') + '?next=' + reverse('logout'))
