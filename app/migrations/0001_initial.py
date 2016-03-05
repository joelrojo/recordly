# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-05 06:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('title', models.CharField(blank=True, max_length=250, unique=True)),
                ('favorited', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=250, unique=True)),
                ('favorited', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('title', models.CharField(blank=True, max_length=250, unique=True)),
                ('favorited', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.Artist'),
        ),
        migrations.AddField(
            model_name='album',
            name='songs',
            field=models.ManyToManyField(blank=True, to='app.Song'),
        ),
    ]
