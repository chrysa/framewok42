# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('profil', '0002_account'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]
