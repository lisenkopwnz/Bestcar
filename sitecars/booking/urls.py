from django.urls import path

from booking.views import Confirmation

app_name = 'users'

urlpatterns = [
                path('confirm/<slug:trip_slug>/', Confirmation.as_view(), name='confirmation'),]