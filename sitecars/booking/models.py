from django.contrib.auth import get_user_model
from django.db import models

from bestcar.models import Publishing_a_trip


class Booking(models.Model):
    """
    Модель для бронирования поездок. Включает информацию о месте отправления
    и прибытия, времени поездки, цене, категории и связанных пользователях
    (автор поездки и пассажир).
    """
    trip: models.ForeignKey = models.ForeignKey(Publishing_a_trip, on_delete=models.CASCADE, related_name="bookings")
    name_companion: models.ForeignKey = models.ForeignKey(
        get_user_model(),
        verbose_name="Имя пассажира",
        on_delete=models.CASCADE,
    )
    slug: str = models.SlugField(
        max_length=100,
        db_index=True,
    )

    class Meta:
        verbose_name = 'зарезервированная поездка'
        verbose_name_plural = 'зарезервированные поездки'
