# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designweb', '0025_auto_20150627_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_promotion',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
