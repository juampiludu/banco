# Generated by Django 3.0.7 on 2020-08-01 04:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banking', '0006_transactions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='cash_sended',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='from_cvu',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='to_cvu',
        ),
        migrations.RemoveField(
            model_name='transactions',
            name='to_user',
        ),
        migrations.AddField(
            model_name='transactions',
            name='cash_moved',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='transactions',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Transferencias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_sended', models.FloatField(default=None)),
                ('from_cvu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_cvu', to='banking.Banking')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_cvu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_cvu', to='banking.Banking')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
