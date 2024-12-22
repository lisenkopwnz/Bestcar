from typing import Dict, Any

from elasticsearch_dsl.search_base import SearchBase
from typing_extensions import Type

from common.elasticsearch.document import PublishingTripDocument
from common.utils.interface.interface import StorageRepository
from elasticsearch_dsl import Search

class ELASTRepository(StorageRepository):
    """
    Универсальный репозиторий для работы с документами Elasticsearch.
    При необходимости данный класс может быть расширен доп. методами
    """

    def __init__(self, document: Type[PublishingTripDocument]) -> None:
        self.document = document

    def create_search_query(self) -> Search:
        """Создаем начальный объект запроса"""
        return self.document.search()

    def filter(self, search_query: SearchBase, filter_type: str, **kwargs: Dict[str, Any]) -> SearchBase:
        """Применяем фильтр к существующему запросу"""
        return search_query.filter(filter_type, **kwargs)

    def exists(self,search_query, **kwargs: Any) -> bool:
        """
        Проверяем на наличие документа в индексе Elasticsearch с использованием фильтрации.
        """
        # Выполняем запрос и проверяем, есть ли результаты
        if search_query.execute().hits.total.value > 0:
            return True
        return False