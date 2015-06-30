# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumCat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Name', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='Name', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Message', models.TextField()),
                ('CreateDate', models.DateTimeField(auto_now_add=True)),
                ('LastModified', models.DateTimeField(auto_now_add=True)),
                ('Autor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ForumTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Title', models.CharField(default='categorie', max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(populate_from='Title', editable=False)),
                ('Message', models.TextField()),
                ('CreateDate', models.DateTimeField(auto_now_add=True)),
                ('LastModified', models.DateTimeField(auto_now_add=True)),
                ('LastReply', models.DateTimeField(auto_now_add=True)),
                ('Autor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('CatParent', models.ForeignKey(related_name='categorie_parente', to='forum.ForumCat')),
            ],
        ),
        migrations.AddField(
            model_name='forumpost',
            name='TopicParent',
            field=models.ForeignKey(to='forum.ForumTopic', null=True),
        ),
    ]
