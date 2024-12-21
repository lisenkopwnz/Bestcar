from abc import ABC, abstractmethod
from typing import Dict, Any, List


class StorageRepository(ABC):
    """ ����������� ����� ������� ���������� ����� ������� ��� ������ � ���������� ����������� ������"""
    @abstractmethod
    def filter(self, **kwargs:Dict[str:Any])-> List[Any]:
        """ ���������� ������ ������� �� ��������� ������"""

    @abstractmethod
    def exists(self, **kwargs: Any)-> bool:
        """ ��������� �������� ������ �� ������� ������"""
        pass
