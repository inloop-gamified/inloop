# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0004_populate_scoped_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='scoped_id',
            field=models.PositiveIntegerField(editable=False, help_text='Solution id unique for task and author'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='solution',
            unique_together=set([('author', 'scoped_id', 'task')]),
        ),
        migrations.AlterIndexTogether(
            name='solution',
            index_together=set([('author', 'scoped_id', 'task')]),
        ),
    ]
