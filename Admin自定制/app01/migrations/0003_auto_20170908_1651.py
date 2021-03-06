# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-08 08:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20170908_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='ug',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Group'),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=32, verbose_name='用户组'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='u2r',
            field=models.ManyToManyField(to='app01.Role', verbose_name='角色'),
        ),
    ]
