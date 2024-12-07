import logging

from django.http import Http404

from .models import Publishing_a_trip


logger = logging.getLogger('duration_request_view')


class TripFilterService:
    """
    Производит фильтрацию на основе параметров который задал пользователь
    в форме на главной странице
    """
    @staticmethod
    def parse_elastic_hits(result):
        """
            Парсит результаты поиска из Elasticsearch и извлекает документы.

            :param result: объект результата поиска, полученный от Elasticsearch.
            :return: список документов (словарей) из поля '_source' каждого хита.
        """
        result = (result.execute().to_dict())
        hits = result['hits']['hits']
        documents = [hit['_source'] for hit in hits]
        return documents

    @staticmethod
    def filter_trip(queryset, data):
        search_query = queryset.query(
            'bool',
            must=[
                {'fuzzy': {'departure': {'value': data['departure'], 'fuzziness': 'AUTO'}}},
                {'fuzzy': {'arrival': {'value': data['arrival'], 'fuzziness': 'AUTO'}}}
            ],
            filter=[
                {'range': {'departure_time': {'gte': data['datetime_value']}}},
                {'range': {'free_seating': {'gte': data['seating']}}}
            ]
        )

        results = TripFilterService.parse_elastic_hits(search_query)
        logger.info(results)
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


def elasticsearch_formatting_date(date):
    """
        Форматирует дату в строку ISO 8601, подходящую для Elasticsearch.

        :param date: объект даты, который необходимо отформатировать.
        :return: строка, представляющая дату в формате ISO 8601.
    """
    return date.isoformat()