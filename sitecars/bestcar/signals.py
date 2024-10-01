from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .decorators import email_address_decorator
from .models.publishing_a_trip import Publishing_a_trip
from .tasks import send_email_task


@receiver(post_save, sender=Publishing_a_trip)
@email_address_decorator
def notify_about_change(sender, instance, created, email_list, **kwargs):
    if not created:
        send_email_task.delay(
            'Убедитесь, что вы используете правильные параметры '
            'SMTP для вашей'
            ,
            'с которой вы отправляете почту, имеет необходимые права и настройки.',
            email_list
        )


@receiver(post_delete, sender=Publishing_a_trip)
@email_address_decorator
def notify_about_delete(sender, instance, email_list, **kwargs):
    send_email_task.delay(
        'Уведомление об удалении поездки',

        f' удвлмл поездку.',
        email_list
    )
