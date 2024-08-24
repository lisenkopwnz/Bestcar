from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from bestcar.models import Publishing_a_trip
from booking.models import Booking
from booking.services import Confirmation_services


class BaseView(View):
    """ Базовый класс который отлавливает все исклюяения ,которые
        не были обработаны ранее """

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return self._response(e, status=400)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(exeption, *, status=200):
        """Форматируем HTTP ответ с описание ошибки"""
        res = JsonResponse({
            "errorMessage": str(exeption),
            "status": status
        })
        return res


class Confirmation(BaseView):
    """
        Создает запись в базе данных о бронировании поездки
    """

    def get(self, request, *args, **kwargs):
        trip_slug = kwargs.get('trip_slug', None)
        if trip_slug is not None:
            try:
                Confirmation_services.confirmation(trip_slug, request)
            except Publishing_a_trip.DoesNotExist as e:
                return JsonResponse({
                    "errorMessage": str(e),
                    "status": 400
                })
            return redirect('home')
