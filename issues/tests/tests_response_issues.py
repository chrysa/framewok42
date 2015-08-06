# -*-coding:utf-8 -*-

from django.test import Client
from django.test import TestCase
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from profil.models import UserLang
from issues.models import Issue


class RespondIssuesTestsLog(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_user = {
            'username': "user_test", 'email': 'user_test@tests.fr', 'password': "tests"}
        self.register_wrong_user = {
            'username': "user_test2", 'email': 'user_test2@tests.fr', 'password': "tests"}
        self.register_admin = {'username': 'admin', 'password': 'admin'}
        self.register_staff = {'username': 'staff', 'password': 'staff'}
        new_user = User.objects.create_user(**self.register_user)
        UserLang.objects.create(user=new_user, lang='fr')
        new_wrong_user = User.objects.create_user(**self.register_wrong_user)
        UserLang.objects.create(user=new_wrong_user, lang='fr')
        new_admin = User.objects.create_user(**self.register_admin)
        User.objects.filter(username=self.register_admin['username']).update(
            is_staff=True, is_superuser=True)
        UserLang.objects.create(user=new_admin, lang='fr')
        new_staff = User.objects.create_user(**self.register_staff)
        User.objects.filter(
            username=self.register_staff['username']).update(is_staff=True)
        UserLang.objects.create(user=new_staff, lang='fr')
        self.TestIssue = {'Autor': User.objects.get(username=self.register_user['username']),
                          'Assign': User.objects.get(username=self.register_admin['username']), 'Title': 'test issue',
                          'UserRequest': 'test content issue'}
        Issue(**self.TestIssue).save()
