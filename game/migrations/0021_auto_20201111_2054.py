# Generated by Django 3.1 on 2020-11-11 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0020_askedquestions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AskedQuestions',
            new_name='AskedQuestion',
        ),
    ]
