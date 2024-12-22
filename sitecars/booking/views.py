import logging

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView

from bestcar.utils import DataMixin
from bestcar.models import Publishing_a_trip
from booking.models import Booking
from booking.services.services import Confirmation_services, UsersBookedTripsServices
from common.utils.base_view import BaseView
from common.utils.repository.django_orm_repository import ORMRepository
from sitecars import settings

logger = logging.getLogger('duration_request_view')


class Bookings(DataMixin, BaseView, DetailView):
    """
        Представление в котором пользователь может ознакомиться с деталями поездки
    """
    model = Publishing_a_trip
    template_name = 'booking/to_book_a_trip.html'
    title_page = 'Потверждение'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, default_image=settings.DEFAULT_USER_IMAGE)


class Checkout(DataMixin, BaseView, DetailView):
    """
         Представление в котором пользователь может проверить детали поездки
    """
    model = Publishing_a_trip
    template_name = 'booking/booking_checkout.html'
    title_page = 'Проверьте детали поездки'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, default_image=settings.DEFAULT_USER_IMAGE)


class Confirmation(BaseView):
    """
        Создает запись в базе данных о бронировании поездки
    """
    @staticmethod
    def get_data(**kwargs):
        return kwargs.get('trip_slug')

    def get(self, request, *args, **kwargs):
        trip_slug = self.get_data(**kwargs)

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
    """
        Добовляет отображения списка забронированных поездок
    """
    context_object_name = 'mein_booked_trip'
    model = Booking
    template_name = 'booking/users_booked_trips.html'
    title_page = 'Ваши забронированные поездки'

    def get_queryset(self):
        return UsersBookedTripsServices.users_booked_trips(name_companion=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class Delete_a_reservation(DataMixin, BaseView, DeleteView):
    """
        Позволяет удалять одну конкретную поездку
    """

    model = Booking
    template_name = 'booking/delete_confirmation.html'
    success_url = reverse_lazy('booking:booked_trips')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Бронирование отменено")
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)
