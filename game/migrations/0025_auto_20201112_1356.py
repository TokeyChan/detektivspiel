# Generated by Django 3.1 on 2020-11-12 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0024_auto_20201112_1241'),
    ]

    operations = [
        migrations.RenameField(
            model_name='askedquestion',
            old_name='person',
            new_name='player',
        ),
    ]
