# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('urlshortener', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PairedUrl',
            fields=[
                ('key_generated', models.OneToOneField(primary_key=True, serialize=False, to='urlshortener.WordList')),
                ('url', models.URLField(unique=True, validators=[django.core.validators.URLValidator()])),
                ('cdate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
