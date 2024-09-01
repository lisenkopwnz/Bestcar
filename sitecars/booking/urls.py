from django.urls import path

from booking.views import Confirmation, Users_booked_trips, Delete_a_reservation, Bookings, Checkout

app_name = 'booking'

urlpatterns = [
    path('to_book/<slug:trip_slug>/', Bookings.as_view(), name='to_book'),
    path('booking/checkout/<slug:slug>/', Checkout.as_view(), name='booking'),
    path('confirm/<slug:trip_slug>/', Confirmation.as_view(), name='confirmation'),
    path('booked_trips/', Users_booked_trips.as_view(), name='booked_trips'),
    path('delete/<int:pk>/', Delete_a_reservation.as_view(), name='delete_reservation')


]
