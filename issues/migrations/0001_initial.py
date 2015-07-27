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
            name='Issue',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('Title', models.CharField(max_length=100, default='titre')),
                ('slug', autoslug.fields.AutoSlugField(
                    populate_from='Title', editable=False)),
                ('UserRequest', models.TextField()),
                ('Answer', models.TextField()),
                ('CreateDate', models.DateTimeField(auto_now_add=True)),
                ('LastActivity', models.DateTimeField(auto_now_add=True)),
                ('Status', models.CharField(choices=[
                    ('open', 'open'), ('progress', 'in_progress'), ('close', 'status')], max_length=20,
                    default='open')),
                ('Assign', models.ForeignKey(
                    related_name='assign', null=True, to=settings.AUTH_USER_MODEL)),
                ('Autor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
