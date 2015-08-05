#-*-coding:utf-8 -*-
"""
:module: forum.admin
:synopsis: define admin panel for forum

:moduleauthor: anthony greau <greau.anthony@gmail.com>
:created: 01/07/2015
:update: 04/08/2015
:seealso: forum.moodels.ForumCat
:seealso: forum.moodels.ForumPost
:seealso: forum.moodels.ForumTopic
:todo: personalise admin panel
"""
from django.contrib import admin

from forum.models import ForumCat
from forum.models import ForumPost
from forum.models import ForumTopic


class TopicAdmin(admin.ModelAdmin):
    ordering = ['CreateDate', 'LastModified']
    list_display = ('CatParent', 'Autor', 'short_title', 'short_message', 'CreateDate', 'LastModified')
    list_display_links = ('CatParent', 'Autor', 'short_title', 'short_message', 'CreateDate', 'LastModified')
    list_filter = ('CatParent', 'Autor')
    search_fields = ['Autor', 'Title', 'Message', 'CreateDate', 'LastModified']

    def short_title(self, Topic):
        if len(Topic.Title) > 40:
            text = Topic.Title[0:40]
            return '%s…' % text
        else:
            return Topic.Title

    def short_message(self, Topic):
        if len(Topic.Message) > 40:
            text = Topic.Message[0:40]
            return '%s…' % text
        else:
            return Topic.Message


class PostAdmin(admin.ModelAdmin):
    ordering = ['CreateDate', 'LastModified']
    list_display = ('TopicParent', 'Autor', 'short_message', 'CreateDate', 'LastModified')
    list_display_links = ('TopicParent', 'Autor', 'short_message', 'CreateDate', 'LastModified')
    list_filter = ('Autor', 'CreateDate', 'LastModified')
    search_fields = ['Autor', 'CreateDate', 'LastModified']

    def short_message(self, Post):
        if len(Post.Message) > 40:
            text = Post.Message[0:40]
            return '%s…' % text
        else:
            return Post.Message

admin.site.register(ForumCat)
admin.site.register(ForumTopic, TopicAdmin)
admin.site.register(ForumPost, PostAdmin)
