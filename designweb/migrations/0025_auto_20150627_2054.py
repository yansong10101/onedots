# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designweb', '0024_auto_20150613_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_alert',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='reviewer',
            field=models.CharField(default='guest', max_length=50),
            preserve_default=True,
        ),
    ]
