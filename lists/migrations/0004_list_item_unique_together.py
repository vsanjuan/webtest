# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20141010_1557'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('list', 'text')]),
        ),
    ]
