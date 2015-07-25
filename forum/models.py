#-*-coding:utf-8 -*-
"""
:module: forum.models
:synopsis: define storage models for forum

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 21/07/2015:
"""
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from autoslug import AutoSlugField


class ForumCat(models.Model):
    """define the storage of category

    :param models.Model: contain all function for define a storage
    :type models.Model: models object
    :var name: content the name of the category
    :var slug: content the slug of the category
    :return: ForumCat object
    :rtype: object
    """
    Name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=_('Name'))

    def __str__(self):
        return self.Name


class ForumTopic(models.Model):
    """define the storage of topics

    :param models.Model: contain all function for define a storage
    :type models.Model: models object
    :var CatParent: content the object of the parent category
    :var Title: title of topic
    :var slug: access slug of the topic
    :var Autor: user object of the autor
    :var Message: content of the topic
    :var CreateDate: create date of the topic
    :var LastModified: last modify date of the topic
    :var LastReply: last reply date of the topic
    :return: ForumTopic object
    :rtype: object
    """
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
    """define the storage of post

    :param models.Model: contain all function for define a storage
    :type models.Model: models object
    :var TopicParent: content the object of the parent topic
    :var Autor: user object of the autor
    :var Message: content of the post
    :var CreateDate: create date of the post
    :var LastModified: last modify date of the post
    :return: ForumPost object
    :rtype: object
    """
    TopicParent = models.ForeignKey(ForumTopic, null=True)
    Autor = models.ForeignKey(User)
    Message = models.TextField()
    CreateDate = models.DateTimeField(auto_now_add=True)
    LastModified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Title
