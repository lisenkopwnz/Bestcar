
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from bestcar.models import Publishing_a_trip
from booking.models import Booking
from booking.services import Confirmation_confirmation


class BaseView(View):

    def dispatch(self, request, *args, **kwargs):
        try:
            print('1')
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({1:e.args})
        return response




class Confirmation(BaseView):
    """
        Создает запись в базе данных о бронировании поездки
    """
    def get(self, request, *args, **kwargs):
        trip_slug = kwargs.get('trip_slug', None)
        if trip_slug is not None:
            try:
                Confirmation_confirmation.confirmation(trip_slug,request)
            except Publishing_a_trip.DoesNotExist:
                pass
            return redirect('home')
