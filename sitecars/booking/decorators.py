import functools
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

from bestcar.models import Publishing_a_trip
from booking.exeption.exeption import SeatingError

logger = logging.getLogger('duration_request_view')

def booking_decorator(func):
    """
    Декоратор принимает функцию confirmation в которой создается запись о бронировании поездки,
        декоратор проверяет наличие свободных мест в опубликованной поездке.
    """
    @functools.wraps(func)
    def wrapper_decorator(trip_slug, request):
        try:
            trip = Publishing_a_trip.objects.select_related('author').get(slug=trip_slug)
            if trip.reserved_seats < trip.free_seating:
                Publishing_a_trip.objects.filter(slug=trip_slug).update(reserved_seats=F('reserved_seats') + 1)
                return func(trip_slug, request, trip)
            else:
                raise SeatingError()
        except ObjectDoesNotExist:
            raise ValueError("Поездка не найдена")
    return wrapper_decorator

