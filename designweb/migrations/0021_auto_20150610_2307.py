# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designweb', '0020_product_manually_set_prior_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_first_name',
            field=models.CharField(default='', max_length=25),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='billing_last_name',
            field=models.CharField(default='', max_length=25),
            preserve_default=True,
        ),
    ]
