from abc import ABC, abstractmethod
from typing import Dict, Any, List


class StorageRepository(ABC):
    """ Абстрактный класс который определяет набор методов для работы с различными источниками данных"""
    @abstractmethod
    def filter(self, **kwargs:Dict[str:Any])-> List[Any]:
        """ Возвращаем список записей из источника данных"""

    @abstractmethod
    def exists(self, **kwargs: Any)-> bool:
        """ Проверяем источник данных на наличие обекта"""
        pass
