# Generated by Django 5.0.1 on 2024-03-21 09:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_onetimeurl_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onetimeurl',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 22, 9, 41, 35, 118618, tzinfo=datetime.timezone.utc)),
        ),
    ]
