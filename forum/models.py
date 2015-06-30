import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from autoslug import AutoSlugField
# import datetime


class ForumCat(models.Model):
    Name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=_('Name'))

    def __str__(self):
        return self.Name


class ForumTopic(models.Model):
    CatParent = models.ForeignKey(ForumCat, related_name=_("categorie_parente"))
    Title = models.CharField(max_length=100, default=_('categorie'))
    slug = AutoSlugField(populate_from='Title')
    Autor = models.ForeignKey(User)
    Message = models.TextField()
    CreateDate = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now_add=True)
    LastReply = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Title


class ForumPost(models.Model):
    TopicParent = models.ForeignKey(ForumTopic, null=True)
    Autor = models.ForeignKey(User)
    Message = models.TextField()
    CreateDate = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now_add=True)
