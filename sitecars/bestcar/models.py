from django.db import models
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
import pytz
import string
import random
from django.urls import reverse
from .validators import *


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
    SEATING = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4')
    ]

    departure = models.CharField(max_length=100, verbose_name="отправление", validators=[Validators_language_model()])
    arrival = models.CharField(max_length=100, verbose_name="прибытие", validators=[Validators_language_model()])
    departure_time = models.DateTimeField(verbose_name="время отправления", validators=[Validators_date_model()])
    arrival_time = models.DateTimeField(verbose_name="время прибытия", default=None,
                                        validators=[Validators_date_model()])
    seating = models.PositiveSmallIntegerField(verbose_name='количество мест', choices=SEATING, default=1)
    cat = models.ForeignKey('Category', verbose_name="категория", on_delete=models.PROTECT, default=1)
    price = models.PositiveSmallIntegerField(verbose_name="цена")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                               related_name="author", null=True, default=None)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    models_auto = models.CharField(max_length=100, verbose_name="модель автомобиля")
    objects = models.Manager()
    car = CarManager()
    bus = BusManager()

    def get_absolute_url(self):
        return reverse('to_book', kwargs={'trip_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            all_symbols = string.ascii_uppercase + string.digits
            self.slug = "".join(random.choice(all_symbols) for i in range(40))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Опубликованные поездки'
        verbose_name_plural = 'Опубликованные поездки'
        ordering = ('departure_time',)

    def __str__(self):
        return str(self.author)





class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")

    def __str__(self):
        return self.name

    def save(self, *args,
             **kwargs):  # Переопределяем метод save, который убирает возможность удаленя поля в админпонели
        if self.name != 'На машине' or 'На автобусе':
            super(Category, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class Publishing_a_tripForm(forms.ModelForm):
    class Meta:
        model = Publishing_a_trip
        fields = ['departure', 'arrival', 'models_auto', 'departure_time', 'arrival_time', 'seating', 'price', 'cat']
        widgets = {'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
                   'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
                   }

        help_texts = {
            'departure': 'Введите место отправления.',
            'arrival': 'Введите место прибытия.',
            'models_auto': 'Введите марку автомобиля.',
            'departure_time': 'Введите время отправления.',
            'arrival_time': 'Введите время прибытия.',
            'seating': 'Введите количество мест.',
            'price': 'Введите цену билета.',
            'cat': 'Выберите категорию.'
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['placeholder'] = field.help_text
