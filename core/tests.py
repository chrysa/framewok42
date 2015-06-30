from django.test import TestCase
from django.core.urlresolvers import reverse


class CoreUrlTests(TestCase):

    def test_home_url(self):
        reponse = self.client.get(reverse('home'))
        self.assertEqual(reponse.status_code, 200)
