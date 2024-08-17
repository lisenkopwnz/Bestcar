from django.db.models import Q

from .models import Publishing_a_trip


class TripFilterService:
    '''
    Производит фильтрацию на основе параметров который задал пользователь
    в форме на главной странице
    '''
    @staticmethod
    def filter_trip(cat, departure, arrival, seating, data):
        filters_map = {
            'На машине ': Publishing_a_trip.car,
            'На автобусе': Publishing_a_trip.bus,
        }

        object_list = filters_map.get(cat, Publishing_a_trip.objects).filter(
            Q(departure__istartswith=departure) &
            Q(arrival__istartswith=arrival) &
            Q(seating__istartswith=seating) &
            Q(departure_time__startswith=data))
        return object_list
