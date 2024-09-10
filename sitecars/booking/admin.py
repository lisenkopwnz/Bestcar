from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class AdminBooking(admin.ModelAdmin):
    pass
