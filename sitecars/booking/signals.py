from typing import List, Type
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from booking.models import Booking
from common.celery.utils.decorators import email_address_decorator
from common.celery.utils.tasks import send_email_task
from common.utils.services.email_services import EmailMessageBuilder
from sitecars import settings


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

        # Создание письма с использованием EmailMessageBuilder
        msg = EmailMessageBuilder(
            subject='Информация о новом попутчике',
            template_name='email.html',
            context={
                'information': f'{instance.name_companion.username} ваш новый попутчик',
                'current_data': now.strftime("%Y-%m-%d %H:%M")
            },
            sender_email=email_list,
            recipient_emails=[settings.EMAIL_HOST_USER]
        )
        message = msg.build_message()

        # Отправка письма через Celery задачу
        send_email_task.delay(message)


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

    :param sender: Класс модели, вызвавшей сигнал.
    :param instance: Экземпляр модели.
    :param email_list: Список email получателей.
    :param kwargs: Дополнительные параметры.
    """
    now = timezone.now()

    # Создание письма с использованием EmailMessageBuilder
    msg = EmailMessageBuilder(
        subject='Уведомление об удалении брони',
        template_name='email.html',
        context={
            'information': f'{instance.name_companion.username} больше не ваш попутчик',
            'current_data': now.strftime("%Y-%m-%d %H:%M")
        },
        sender_email=email_list,
        recipient_emails=[settings.EMAIL_HOST_USER]
    )
    message = msg.build_message()

    # Отправка письма через Celery задачу
    send_email_task.delay(message)
