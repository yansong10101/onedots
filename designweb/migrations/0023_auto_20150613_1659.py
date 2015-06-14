# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designweb', '0022_auto_20150613_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='number_items',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
