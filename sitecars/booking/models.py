from django.contrib.auth import get_user_model
from django.db import models

from bestcar.models import Category

from bestcar.validators import Validators_date_model, Validators_language_model


class Booking(models.Model):

    departure = models.CharField(max_length=100, verbose_name="отправление", validators=[Validators_language_model()])
    arrival = models.CharField(max_length=100, verbose_name="прибытие", validators=[Validators_language_model()])
    departure_time = models.DateTimeField(verbose_name="время отправления", validators=[Validators_date_model()])
    arrival_time = models.DateTimeField(verbose_name="время прибытия", default=None,validators=[Validators_date_model()])
    cat = models.ForeignKey('bestcar.Category', verbose_name="категория", on_delete=models.PROTECT,default=1)
    price = models.PositiveSmallIntegerField(verbose_name="цена")
    author_trip = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="autho", null=True)
    name_companion=models.ForeignKey(get_user_model(), verbose_name="Имя пассажира",on_delete=models.CASCADE,default='default')
    slug = models.SlugField(max_length=100,  db_index=True)

    class Meta:
        verbose_name = 'зарезервированные поездки'
        verbose_name_plural = 'зарезервированные поездки'
