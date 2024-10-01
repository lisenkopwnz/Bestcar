import functools
from booking.models import Booking


def email_address_decorator(func):
    @functools.wraps(func)
    def wrapper(sender, instance, created=None, **kwargs):
        email_list = (
            Booking.objects
            .select_related('name_companion')
            .filter(slug=instance.slug)
            .values_list('name_companion__email', flat=True)
        )

        # Преобразуем QuerySet в список
        email_list = list(email_list)

        match created:
            case None:
                return func(sender, instance, email_list, **kwargs)
            case _:
                return func(sender, instance, created, email_list, **kwargs)

    return wrapper
