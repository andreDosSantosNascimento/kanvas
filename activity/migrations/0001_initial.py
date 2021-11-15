# Generated by Django 3.2.9 on 2021-11-15 00:04

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(null=True)),
                ('repo', models.CharField(max_length=255)),
                ('user_id', models.IntegerField()),
                ('activity_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('points', models.IntegerField(verbose_name=django.contrib.auth.models.User)),
                ('submissions', models.ManyToManyField(related_name='submissions', to='activity.Submission')),
            ],
        ),
    ]
