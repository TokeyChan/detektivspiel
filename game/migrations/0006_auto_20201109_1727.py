# Generated by Django 3.1 on 2020-11-09 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_itemmeta_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('html_id', models.CharField(max_length=100)),
                ('background_img', models.CharField(max_length=100)),
                ('visitable_by_default', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='itemmeta',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('is_suspect', models.BooleanField(default=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.place')),
            ],
        ),
    ]
