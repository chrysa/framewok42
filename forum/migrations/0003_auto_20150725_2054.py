# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0002_auto_20150725_2028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forumcat',
            old_name='NameCat',
            new_name='Name',
        ),
    ]
