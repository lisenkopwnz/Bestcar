# Generated by Django 5.0.7 on 2024-09-18 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='models_auto',
            field=models.CharField(default=1, max_length=100, verbose_name='модель автомобиля'),
            preserve_default=False,
        ),
    ]
