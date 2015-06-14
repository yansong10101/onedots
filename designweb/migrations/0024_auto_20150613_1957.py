# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designweb', '0023_auto_20150613_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='number_items',
            field=models.IntegerField(blank=True, default=1, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='order',
            field=models.ForeignKey(to='designweb.Order', editable=False, related_name='details'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='product',
            field=models.ForeignKey(to='designweb.Product', editable=False, related_name='products'),
            preserve_default=True,
        ),
    ]
