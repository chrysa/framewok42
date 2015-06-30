from django.db import models
from django.contrib.auth.models import User

class UserLang(models.Model):
    user = models.ForeignKey(User)
    lang = models.CharField(max_length=3)
