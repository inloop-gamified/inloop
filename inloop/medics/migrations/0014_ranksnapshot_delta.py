# Generated by Django 2.2.13 on 2020-08-10 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medics', '0013_ranksnapshot'),
    ]

    operations = [
        migrations.AddField(
            model_name='ranksnapshot',
            name='delta',
            field=models.IntegerField(default=0),
        ),
    ]
