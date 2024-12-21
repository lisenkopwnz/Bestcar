import logging
from typing import List, Type
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from booking.models import Booking
from common.celery.utils.decorators import email_address_decorator
from common.celery.utils.tasks import send_email_task
from sitecars import settings

logger = logging.getLogger('duration_request_view')

@receiver(post_save, sender=Booking)
@email_address_decorator(model=Booking)
def notify_about_new_companion(
                        sender: Type[Booking],
                        instance: Booking,
                        created: bool,
                        email_list: List[str],
                        **kwargs: dict
                    ) -> None:
    """
    Уведомляет автора поездки о новом попутчике.
    """
    if created:
        now = timezone.now()
        from_email = settings.EMAIL_HOST_USER
        logger.info(from_email,email_list)

        # Передаем данные в задачу Celery
        send_email_task.delay(
            subject='Информация об изменении в параметрах поездки',
            template_name = 'email.html',
            context={
                'information': f'{instance.name_companion.username} ваш новый попутчик',
                'current_data': now.strftime("%Y-%m-%d %H:%M")
            },
            sender_email=from_email,
            recipient_emails=email_list
        )


@receiver(post_delete, sender=Booking)
@email_address_decorator(model=Booking)
def notify_about_booking_deletion(
                        sender: Type[Booking],
                        instance: Booking,
                        email_list: List[str],
                        **kwargs: dict
                    ) -> None:
    """
    Уведомляет участников поездки об удалении брони.
    """
    now = timezone.now()
    from_email = settings.EMAIL_HOST_USER

    # Передаем данные в задачу Celery
    send_email_task.delay(
        subject='Информация об изменении в параметрах поездки',
        template_name='email.html',
        context={
            'information': f'{instance.name_companion.username} больше не ваш попутчик',
            'current_data': now.strftime("%Y-%m-%d %H:%M")
        },
        sender_email=from_email,
        recipient_emails=email_list
    )
