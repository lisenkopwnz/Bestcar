import functools
from booking.models import Booking


def email_address_decorator(func):
    @functools.wraps(func)
    def wrapper(sender, instance, created, **kwargs):
        email_list = (
            Booking.objects
            .select_related('name_companion')
            .filter(slug=instance.slug)
            .values_list('name_companion__email', flat=True)
        )

        # Преобразуем QuerySet в список
        email_list = list(email_list)

        return func(sender, instance, created, email_list, **kwargs)

    return wrapper
