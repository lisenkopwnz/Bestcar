from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404

from common.elasticsearch.document import PublishingTripDocument
from .models import Publishing_a_trip


class TripFilterService:
    """
    Производит фильтрацию на основе параметров который задал пользователь
    в форме на главной странице
    """

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

        results = search_query.execute()
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
    return date.strftime('%Y-%m-%dT%H:%M:%SZ')