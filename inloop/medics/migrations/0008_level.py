# Generated by Django 2.2.13 on 2020-08-04 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medics', '0007_auto_20200804_1043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('index', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('points', models.PositiveIntegerField()),
                ('name', models.TextField()),
            ],
        ),
    ]
