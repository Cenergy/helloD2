# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-10-10 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': '用户信息', 'verbose_name_plural': '用户信息'},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='faceid',
            field=models.TextField(blank=True, null=True, verbose_name='用户唯一值'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='knowfacecode',
            field=models.TextField(blank=True, null=True, verbose_name='用户人脸矩阵'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_name',
            field=models.TextField(blank=True, null=True, verbose_name='用户名'),
        ),
    ]
