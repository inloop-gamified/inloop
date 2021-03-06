# Generated by Django 2.2.13 on 2020-08-10 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medics', '0012_badge_badgescore'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankSnapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveIntegerField()),
                ('player', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medics.PlayerDetails')),
            ],
        ),
    ]
