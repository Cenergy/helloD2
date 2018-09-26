# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-09-21 23:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0003_sourcescore_question_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceLimit',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('num_count', models.IntegerField(default=50, verbose_name='次数')),
                ('limit_time', models.DateField(default=datetime.date.today, verbose_name='有效时间')),
            ],
        ),
        migrations.AlterField(
            model_name='sourcescore',
            name='code',
            field=models.CharField(blank=True, help_text='可不填，会自动从资源描述里读取', max_length=20, null=True, verbose_name='提取码'),
        ),
        migrations.AlterField(
            model_name='sourcescore',
            name='sourcedesc',
            field=models.CharField(blank=True, help_text='默认是百度云的资源，如果不是，上面两个请填写', max_length=200, null=True, verbose_name='综合描述'),
        ),
        migrations.AlterField(
            model_name='sourcescore',
            name='sourceurl',
            field=models.URLField(blank=True, help_text='可不填，会自动从资源描述里读取', null=True, verbose_name='资源地址'),
        ),
    ]