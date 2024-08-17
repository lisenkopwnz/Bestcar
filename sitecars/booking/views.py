from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from bestcar.models import Publishing_a_trip
from booking.models import Booking


class Confirmation(View):
    def get(self, request, *args, **kwargs):
        trip_slug = kwargs.get('trip_slug', None)
        if trip_slug is not None:
            try:
                with transaction.atomic():
                    # Попытка найти запись с заданными значением слага
                    trip = Publishing_a_trip.objects.get(slug=trip_slug)
                    print(trip.cat)

                    # Создаем новую запись
                    booking = Booking(departure=trip.departure,
                                      arrival=trip.arrival,
                                      departure_time=trip.departure_time,
                                      arrival_time=trip.arrival_time,
                                      seating=trip.seating,
                                      price=trip.price,
                                      cat=trip.cat,
                                      author=trip.author,
                                      slug=trip.slug
                                      )
                    print(booking.cat)
                    booking.save()

            except Publishing_a_trip.DoesNotExist:
                pass
            return redirect('home')
