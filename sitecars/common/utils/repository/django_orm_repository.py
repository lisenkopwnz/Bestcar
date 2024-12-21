from typing import Any, Type, Dict, List

from django.db.models import Model, QuerySet, Prefetch

from common.utils.interface.interface import StorageRepository


class ORMRepository(StorageRepository):
    """
        Универсальный репозиторий для работы с моделями.
        При необходимости данный класс может быть расширен доп. методами
    """

    def __init__(self, model: Type[Model]) -> None:
        self.model = model

    def filter(self, **kwargs:Dict[str,Any]) -> List[Any]:
        """ Возвращаем список записей из базы данных с помощью джанго ORM"""
        if not kwargs:
            return self.model.objects.all()
        return self.model.objects.filter(**kwargs)

    def exists(self, **kwargs: Any)-> bool:
        """ Проверяем на наличие обекта в базе данных с помощью джанго ORM"""
        return self.model.objects.filter(**kwargs).exists()
