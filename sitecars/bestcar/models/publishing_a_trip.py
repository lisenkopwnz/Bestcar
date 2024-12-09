from django.db import models
from django.contrib.auth import get_user_model

from bestcar.managers import CarManager, BusManager, ObjectManager
from bestcar.services.services import generate_slug
from bestcar.validators import Validators_date_model
from common.utils.validators import address_validator


class Publishing_a_trip(models.Model):
    """
        Модель, представляющая информацию о поездке.

        Attributes:
            departure (str): Место отправления.
            arrival (str): Место прибытия.
            departure_time (datetime): Время отправления.
            arrival_time (datetime): Время прибытия.
            free_seating (int): Количество свободных мест в транспорте.
            reserved_seats (int): Количество забронированных мест.
            price (int): Стоимость поездки.
            author (ForeignKey): Автор поездки (пользователь).
            slug (str): Уникальный идентификатор поездки.
    """
    departure: str = models.CharField(
        max_length=150,
        verbose_name="отправление",
        validators=[
            address_validator
        ]
    )
    arrival: str = models.CharField(
        max_length=150,
        verbose_name="прибытие",
        validators=[
            address_validator
        ]
    )
    departure_time = models.DateTimeField(
        verbose_name="время отправления",
        validators=[Validators_date_model()],
    )
    arrival_time = models.DateTimeField(
        verbose_name="время прибытия",
        default=None,
        validators=[Validators_date_model()],
    )
    free_seating: int = models.PositiveSmallIntegerField(
        verbose_name='количество мест',
        default=1,
    )
    reserved_seats: int = models.PositiveIntegerField(
        verbose_name='количество бронированных мест',
        default=0,
    )
    price: int = models.PositiveSmallIntegerField(
        verbose_name="цена",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="author",
    )
    slug: str = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    objects = ObjectManager()
    car = CarManager()
    bus = BusManager()

    def save(self, *args, **kwargs):
        """
        Переопределяет метод сохранения для автоматической генерации slug,
        если он отсутствует.
        """
        if not self.slug:
            self.slug = generate_slug(100)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Опубликованные поездки'
        verbose_name_plural = 'Опубликованные поездки'
        ordering = ('departure_time',)

    def __str__(self) -> str:
        """
        Возвращает строковое представление модели.

        Returns:
            str: Имя автора поездки.
        """
        return str(self.author)