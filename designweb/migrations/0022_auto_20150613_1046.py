# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designweb', '0021_auto_20150610_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone1',
            field=models.CharField(max_length=15, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone2',
            field=models.CharField(max_length=15, blank=True),
            preserve_default=True,
        ),
    ]
