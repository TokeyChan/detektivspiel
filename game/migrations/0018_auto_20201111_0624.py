# Generated by Django 3.1 on 2020-11-11 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_auto_20201111_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='sent_away_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
