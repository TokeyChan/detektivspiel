# Generated by Django 3.1 on 2020-11-14 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0025_auto_20201112_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='causedevent',
            name='finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='askedquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.question'),
        ),
        migrations.AlterField(
            model_name='causedevent',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.event'),
        ),
    ]