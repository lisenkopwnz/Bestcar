import logging
from typing import Dict, Any, List

from django.http import Http404
from elasticsearch_dsl import Search
from elasticsearch_dsl.search_base import SearchBase

from bestcar.models import Publishing_a_trip

logger = logging.getLogger('duration_request_view')


class TripFilterService:
    """
    Производит фильтрацию на основе параметров который задал пользователь
    в форме на главной странице
    """
    def __init__(self,queryset: SearchBase, data: Dict[str, Any]) -> None:
        """
               Конструктор для инициализации объекта с queryset и данными.

               :param queryset: Запрос к Elasticsearch (объект Search).
               :param data: Словарь данных с ключами типа str и значениями любого типа.
        """
        self.queryset = queryset
        self.data = data

    @staticmethod
    def parse_elastic_hits(result: Search) -> List[Dict[str, Any]]:
        """
            Парсит результаты поиска из Elasticsearch и извлекает документы.

            :param result: объект результата поиска, полученный от Elasticsearch.
            :return: список документов (словарей) из поля '_source' каждого хита.
        """
        result = (result.execute().to_dict())
        hits = result['hits']['hits']
        documents = [hit['_source'] for hit in hits]
        return documents


    def filter_trip(self)-> List[Dict[str, Any]]:
        """
            Основной метод для фильтрации поездок
        :return:
        """
        search_query = self.queryset.query(
            'bool',
            must=[
                {'fuzzy': {'departure': {'value': self.data['departure'], 'fuzziness': 'AUTO'}}},
                {'fuzzy': {'arrival': {'value': self.data['arrival'], 'fuzziness': 'AUTO'}}}
            ],
            filter=[
                {'range': {'departure_time': {'gte': self.data['datetime_value']}}},
                {'range': {'free_seating': {'gte': self.data['seating']}}}
            ]
        )

        results = TripFilterService.parse_elastic_hits(search_query)
        return results


class User_trip_object:
    """
        Проверякм объект поездки на существование
    """

    @staticmethod
    def users_trip_object(slug: str) -> None:
        if Publishing_a_trip.objects.filter(slug=slug).exists():
            return
        else:
            raise Http404('Похоже эта поездка больше не существует')