from django.urls import path
from .views import (HomeBestcar, SearchTrip, Post, Bus_trip, Car_trip,Update_user_trip,
                    About)

urlpatterns = [
    path('', HomeBestcar.as_view(), name='home'),
    path('search/', SearchTrip.as_view(), name='search'),
    path('post/', Post.as_view(), name='post'),
    path('bus_trip/', Bus_trip.as_view(), name='bus_trip'),
    path('car_trip/', Car_trip.as_view(), name='car_trip'),
    path('update/<slug:slug>/', Update_user_trip.as_view(), name='update_user_trip'),
    path('about/', About.as_view(), name='about'),
]
