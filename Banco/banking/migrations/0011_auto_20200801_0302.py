# Generated by Django 3.0.7 on 2020-08-01 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0010_auto_20200801_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.CharField(default='1 de Agosto del 2020 - 03:2', max_length=60),
        ),
        migrations.AlterField(
            model_name='transferencias',
            name='date',
            field=models.CharField(default='1 de Agosto del 2020 - 03:2', max_length=60),
        ),
    ]
