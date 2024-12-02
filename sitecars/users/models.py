from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from bestcar.models import Category


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name= 'Имя пользователя',
        max_length=150,
        validators=[username_validator]
    )
    photo = models.ImageField(
        upload_to='users/$Y/%m/%d/',
        verbose_name='Фотография',
    )
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
    phone_number = PhoneNumberField(
        unique=True,
        verbose_name='Номер телефона',
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Адрес электронной почты"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
