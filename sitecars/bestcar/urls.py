from django.urls import path

from . import views
from .views import (HommeBestcar, SearchTrip, Post, Bus_trip, Car_trip,
                    Bookings,About,Checkout)

urlpatterns = [
    path('', HommeBestcar.as_view(), name='home'),
    path('search/', SearchTrip.as_view(), name='search'),
    path('post/', Post.as_view(), name='post'),
    path('bus_trip/', Bus_trip.as_view(), name='bus_trip'),
    path('car_trip/', Car_trip.as_view(), name='car_trip'),
    path('about/', About.as_view(), name='about'),
    path('to_book/<slug:trip_slug>/',Bookings.as_view(), name='to_book'),
    path('booking/checkout/<slug:slug>/', Checkout.as_view(), name='booking'),




]
