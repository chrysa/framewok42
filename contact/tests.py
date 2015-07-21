from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from profil.models import UserLang


class ContactTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_user = {
            'username': "user_test",
            'email': 'user_test@test.fr',
            'password': "test",
            'lang': 'fr',
        }

        unittest_fr = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=unittest_fr, lang=self.register_user['lang'])

    def test_contact_url(self):
        reponse = self.client.get(reverse('contact'))
        print (reponse.context)
        self.assertEqual(reponse.status_code, 200)

# envoi de contact non connecte
# envoi de contact non connecte vide
# envoi de contact non connecte bad password
# envoi de contact connecte
# envoi de contact connecte vide