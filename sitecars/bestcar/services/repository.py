from typing import Any, Type

from django.db.models import Model


class Repository:
    """
        Универсальный репозиторий для работы с моделями.
        При необходимости данный класс может быть расширен доп. методами
    """

    def __init__(self, model: Type[Model]) -> None:
        self.model = model

    def exists(self, **kwargs: Any)-> bool:
        """ Проверяем модель на наличие обекта"""
        return self.model.objects.filter(**kwargs).exists()
