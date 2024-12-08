from django.db import models


class CarManager(models.Manager):
    """
    Кастомный менеджер для фильтрации поездок с категорией 'Автобус'.
    """
    def get_queryset(self):
        return super().get_queryset().filter(cat_id=1)


class BusManager(models.Manager):
    """
    Кастомный менеджер для фильтрации поездок с категорией 'Автомобиль'.
    """
    def get_queryset(self):
        return super().get_queryset().filter(cat_id=2)


class ObjectManager(models.Manager):
    """
    Кастомный менеджер для получения всех записей.
    """
    def get_queryset(self):
        return super().get_queryset().all()
