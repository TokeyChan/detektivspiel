# Generated by Django 3.1 on 2020-11-11 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_auto_20201111_0624'),
    ]

    operations = [
        migrations.CreateModel(
            name='InspectorText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('causes_event', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='caused_by_inspector', to='game.event')),
                ('on_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='causes_inspector', to='game.event')),
            ],
        ),
    ]
