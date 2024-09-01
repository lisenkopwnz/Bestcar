from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Publishing_a_trip



class TripFilterService:
    """
    Производит фильтрацию на основе параметров который задал пользователь
    в форме на главной странице
    """

    @staticmethod
    def filter_trip(cat, departure, arrival, free_seating, data):
        filters_map = {
            'На машине ': Publishing_a_trip.car,
            'На автобусе': Publishing_a_trip.bus,
        }

        object_list = filters_map.get(cat, Publishing_a_trip.objects).filter(
            Q(departure__istartswith=departure) &
            Q(arrival__istartswith=arrival) &
            Q(free_seating__istartswith=free_seating) &
            Q(departure_time__startswith=data))
        return object_list


class User_trip_object:
    """
        Возвращает объект поездки если таковой существует
    """
    @staticmethod
    def users_trip_object(slug):
        try:
            return get_object_or_404(Publishing_a_trip, slug=slug)
        except Exception:
            raise Http404('Похоже эта поездка болше не существует')
