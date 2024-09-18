from django.db import models
from django.contrib.auth import get_user_model

import string
import random

from bestcar.validators import Validators_date_model,Validators_language_model


class CarManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(cat_id=1)


class BusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(cat_id=2)


class ObjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()


class Publishing_a_trip(models.Model):
    departure = models.CharField(
        max_length=100,
        verbose_name="отправление",
        validators=[Validators_language_model()]
    )
    arrival = models.CharField(
        max_length=100,
        verbose_name="прибытие",
        validators=[Validators_language_model()]
    )
    departure_time = models.DateTimeField(
        verbose_name="время отправления",
        validators=[Validators_date_model()]
    )
    arrival_time = models.DateTimeField(
        verbose_name="время прибытия",
        default=None,
        validators=[Validators_date_model()]
    )
    free_seating = models.PositiveSmallIntegerField(
        verbose_name='количество мест',
        default=1
    )
    reserved_seats = models.PositiveIntegerField(
        verbose_name='количество бронированных мест',
        default=0
    )
    price = models.PositiveSmallIntegerField(
        verbose_name="цена"
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="author",
        null=True, default=None
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True
    )

    objects = models.Manager()
    car = CarManager()
    bus = BusManager()

    def save(self, *args, **kwargs):
        """ Переопределяем метод save для добавления слага"""
        if not self.slug:
            all_symbols = string.ascii_uppercase + string.digits
            self.slug = "".join(random.choice(all_symbols) for i in range(40))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Опубликованные поездки'
        verbose_name_plural = 'Опубликованные поездки'
        ordering = ('departure_time',)

        indexes = [
            models.Index(
                fields=['departure', 'arrival', 'free_seating', 'departure_time'],
                name='trip_filter_idx'
            )
        ]

    def __str__(self):
        return str(self.author)
