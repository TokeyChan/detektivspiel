# Generated by Django 3.1 on 2020-11-14 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0031_auto_20201114_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectortext',
            name='parenttext',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_text', to='game.inspectortext'),
        ),
    ]
