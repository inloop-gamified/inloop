# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 14:36
from __future__ import unicode_literals

from django.db import migrations


def populate_scoped_ids(apps, schema_editor):
    User = apps.get_model("auth.User")
    Solution = apps.get_model("solutions.Solution")
    Task = apps.get_model("tasks.Task")

    # ugly, but it works!
    for user in User.objects.all():
        for task in Task.objects.all():
            qs = Solution.objects.filter(task=task, author=user)
            for counter, solution in enumerate(qs, start=1):
                solution.scoped_id = counter
                solution.save()


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0003_add_scoped_id'),
    ]

    operations = [
        migrations.RunPython(populate_scoped_ids, reverse_code=migrations.RunPython.noop),
    ]
