# Generated by Django 3.1 on 2020-11-14 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0030_inspectortext_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectortext',
            name='on_event',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='causes_inspector', to='game.event'),
        ),
    ]
