# Generated by Django 3.1 on 2020-11-14 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0034_auto_20201114_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectortext',
            name='text',
            field=models.CharField(max_length=600),
        ),
    ]