# Generated by Django 3.1 on 2020-11-14 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0037_player_cafe_visitable'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspectortext',
            name='HTMLInput',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='inspectortext',
            name='HTMLValue',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]