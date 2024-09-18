from django.db import models

from django.contrib.auth.models import AbstractUser

from bestcar.models import Category


class User(AbstractUser):
    photo = models.ImageField(
        upload_to='users/$Y/%m/%d/',
        blank=True, null=True,
        verbose_name='Фотография')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        default=1,
        verbose_name='Категория транспортного средства'
                                                                                           )
    models_auto = models.CharField(
        max_length=100,
        verbose_name="модель автомобиля"
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
