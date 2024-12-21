from typing import Any, Type, Dict, List

from django.db.models import Model

from common.utils.interface.interface import StorageRepository


class ORMRepository(StorageRepository):
    """
        ������������� ����������� ��� ������ � ��������.
        ��� ������������� ������ ����� ����� ���� �������� ���. ��������
    """

    def __init__(self, model: Type[Model]) -> None:
        self.model = model

    def filter(self, **kwargs:Dict[str:Any]) -> List[Any]:
        """ ���������� ������ ������� �� ���� ������ � ������� ������ ORM"""
        return self.model.objects.filter(**kwargs)

    def exists(self, **kwargs: Any)-> bool:
        """ ��������� �� ������� ������ � ���� ������ � ������� ������ ORM"""
        return self.model.objects.filter(**kwargs).exists()
