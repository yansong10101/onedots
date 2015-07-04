# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designweb', '0026_category_is_promotion'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='percentage_off',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='sales_price',
            field=models.DecimalField(default=0.0, max_digits=7, decimal_places=2),
            preserve_default=True,
        ),
    ]
