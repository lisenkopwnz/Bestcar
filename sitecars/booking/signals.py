from django.db.models.signals import post_delete
from django.dispatch import receiver


from booking.models import Booking
from sitecars.utils.tasks import send_email_task
from sitecars.utils.decorators import email_address_decorator


@receiver(post_delete, sender=Booking)
@email_address_decorator(model=Booking)
def notify_about_delete(sender, instance, email_list, **kwargs):
    send_email_task.delay(
        'Уведомление об удалении поездки',

        f' удвлмл поездку.',
        email_list
    )


@receiver(post_delete, sender=Booking)
@email_address_decorator(model=Booking)
def notify_about_delete(sender, instance, email_list, **kwargs):
    """ Сигнал который оповещает пользовотелей забронировавших поездку об удалении
        поездки автором роздки.
    """
    send_email_task.delay(
        'Уведомление об удалении поездки',

        f' удвлмл поездку.',
        email_list
    )
