from django.core.validators import FileExtensionValidator
from django.db import models

from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from bestcar.models import Category
from common.utils.validators import name_validator, model_auto_validator


class User(AbstractUser):
    """
    Расширенная модель пользователя. Включает дополнительную информацию,
    такую как фотография, категория транспортного средства, модель автомобиля,
    номер телефона и уникальный адрес электронной почты.
    """
    username: str = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        validators=[name_validator]
    )
    photo: models.ImageField = models.ImageField(
        upload_to='users/$Y/%m/%d/',
        verbose_name='Фотография',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png'],
                message='Можно загружать только файлы форматов: JPG, JPEG, PNG.'
            )
        ],
    )
    category: models.ForeignKey = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        default=1,
        verbose_name='Категория транспортного средства'
    )
    models_auto: str = models.CharField(
        max_length=100,
        verbose_name="Модель автомобиля",
        validators=[model_auto_validator]
    )
    phone_number: PhoneNumberField = PhoneNumberField(
        unique=True,
        verbose_name='Номер телефона',
    )
    email: str = models.EmailField(
        unique=True,
        verbose_name="Адрес электронной почты"
    )

    # Настройки для аутентификации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'