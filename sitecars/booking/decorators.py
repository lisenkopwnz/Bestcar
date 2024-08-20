import functools

from bestcar.models import Publishing_a_trip
from .exeption import SeatingError


def booking_decorator(func):
    """
    Декоратор принимает функцию confirmation в которой создается запись о бронировании поездки,
    декоратор проверяет наличие свободных мест в опубликованной поездке.
    :param func: trip_slug - уникальный слаг поездки, request - в котором содержится информация
        о пользователи ,который бронирует поездку.
    :return: в зависимости от результата условного оператора возвращает либо функцию ,либо
        пользовательское исключение.
    """
    @functools.wraps(func)
    def wrapper_decorator(trip_slug, request):
        trip = Publishing_a_trip.objects.get(slug=trip_slug)
        if trip.reserved_seats < trip.free_seating:
            trip.reserved_seats += 1
            trip.save()
            return func(trip_slug, request, trip)
        else:
            raise SeatingError

    return wrapper_decorator
