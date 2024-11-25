# Generated by Django 5.0.7 on 2024-11-25 17:00

import bestcar.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='arrival_time',
            field=models.DateTimeField(validators=[bestcar.validators.Validators_date_model()], verbose_name='время прибытия'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='author_trip',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='author_trip', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
