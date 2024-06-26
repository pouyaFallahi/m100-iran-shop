# Generated by Django 5.0.1 on 2024-01-29 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_observer',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_operator',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_supervisor',
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='is active'),
        ),
    ]
