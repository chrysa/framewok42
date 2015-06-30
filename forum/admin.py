# -- coding: utf-8 --
from django.contrib import admin
from forum.models import ForumCat
from forum.models import ForumPost
from forum.models import ForumTopic


admin.site.register(ForumCat)
admin.site.register(ForumTopic)
admin.site.register(ForumPost)
