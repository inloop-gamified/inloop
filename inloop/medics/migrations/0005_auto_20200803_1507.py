# Generated by Django 2.2.13 on 2020-08-03 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('solutions', '0007_merge_20190802_1345'),
        ('medics', '0004_auto_20200803_1504'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SolutionScore',
            new_name='SolutionPassedScore',
        ),
        migrations.CreateModel(
            name='SolutionViolationScore',
            fields=[
                ('score_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='medics.Score')),
                ('solution', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='solutions.Solution')),
            ],
            bases=('medics.score',),
        ),
    ]
