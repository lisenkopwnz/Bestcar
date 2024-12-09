from django.contrib.auth import get_user_model
from django.db import models

from bestcar.validators import Validators_date_model
from common.utils.validators import address_validator


class Booking(models.Model):
    """
    Модель для бронирования поездок. Включает информацию о месте отправления
    и прибытия, времени поездки, цене, категории и связанных пользователях
    (автор поездки и пассажир).
    """
    departure: str = models.CharField(
        max_length=150,
        verbose_name="отправление",
        validators=[address_validator]
    )
    arrival: str = models.CharField(
        max_length=150,
        verbose_name="прибытие",
        validators=[address_validator]
    )
    departure_time: models.DateTimeField = models.DateTimeField(
        verbose_name="время отправления",
        validators=[Validators_date_model()]
    )
    arrival_time: models.DateTimeField = models.DateTimeField(
        verbose_name="время прибытия",
        validators=[Validators_date_model()]
    )
    cat: models.ForeignKey = models.ForeignKey(
        'bestcar.Category',
        verbose_name="категория",
        on_delete=models.PROTECT,
        default=1
    )
    price: int = models.PositiveSmallIntegerField(
        verbose_name="цена"
    )
    author_trip: models.ForeignKey = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="author_trip"
    )
    name_companion: models.ForeignKey = models.ForeignKey(
        get_user_model(),
        verbose_name="Имя пассажира",
        on_delete=models.CASCADE
    )
    slug: str = models.SlugField(
        max_length=100,
        db_index=True
    )

    class Meta:
        verbose_name = 'зарезервированная поездка'
        verbose_name_plural = 'зарезервированные поездки'
