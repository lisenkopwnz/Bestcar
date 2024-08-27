from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView

from bestcar.models import Publishing_a_trip
from booking.models import Booking
from booking.services import Confirmation_services, UsersBookedTripsServices

from bestcar.utils import DataMixin


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
    def _response(data, *, status=200):
        """Форматируем HTTP ответ с описание ошибки или формируем JSON ответ в случае необходимости """
        if status != 200:
            res = JsonResponse({
                "errorMessage": str(data),
                "status": status
            })
        else:
            res = JsonResponse({
                "data": str(data),
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


class Users_booked_trips(DataMixin, BaseView, ListView):
    context_object_name = 'mein_booked_trip'
    model = Booking
    template_name = 'booking/users_booked_trips.html'
    title_page = 'Ваши забронированные поездки'

    def get_queryset(self):
        return UsersBookedTripsServices.users_booked_trips(name_companion=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class Delete_a_reservation(BaseView,DeleteView):
    model = Booking
    template_name = 'booking/delete_confirmation.html'
    success_url = reverse_lazy('booking:booked_trips')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Task deleted!")
        return super().post(request, *args, **kwargs)


