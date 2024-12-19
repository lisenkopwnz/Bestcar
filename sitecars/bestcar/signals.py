from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from common.celery.utils.decorators import email_address_decorator
from common.utils.services.email_services import EmailMessageBuilder
from common.celery.utils.tasks import send_email_task

from sitecars import settings

from .models.publishing_a_trip import Publishing_a_trip

from typing import List, Type


@receiver(post_save, sender=Publishing_a_trip)
@email_address_decorator(model=Publishing_a_trip)
def notify_about_change(
                    sender: Type[Publishing_a_trip],
                    instance: Publishing_a_trip,
                    created: bool,
                    email_list: List[str],
                    **kwargs: dict
                    ) -> None:
    """
    Сигнал, который оповещает пользователей о изменениях в поездке.
    """
    if not created:
        # получаем текущую дату и время
        now = timezone.now()
        from_email = settings.EMAIL_HOST_USER

        # Создаём сообщение с помощью EmailMessageBuilder
        msg = EmailMessageBuilder(
            subject = 'Информация об изменении в параметрах поездки',
            template_name = 'email.html',
            context = {
                'information': f'Ваш водитель {instance.author.username} изменил условия поездки',
                'current_data': now.strftime("%Y-%m-%d %H:%M")
            },
            sender_email = email_list,
            recipient_emails = from_email
        )
        message = msg.build_message()

        # Передаём сообщение в Celery задачу для отправки
        send_email_task.delay(message)


@receiver(post_delete, sender=Publishing_a_trip)
@email_address_decorator(model=Publishing_a_trip)
def notify_about_delete(
                    sender: Type[Publishing_a_trip],
                    instance: Publishing_a_trip,
                    email_list: List[str],
                    **kwargs: dict
                ) -> None:
    """ Сигнал который оповещает пользовотелей забронировавших поездку об удалении
        поездки автором роздки.
    """
    # получаем текущую дату и время
    now = timezone.now()
    from_email = settings.EMAIL_HOST_USER

    # Создаём сообщение с помощью EmailMessageBuilder
    msg = EmailMessageBuilder(
        subject='Информация об изменении в параметрах поездки',
        template_name='email.html',
        context={
        'information': f'{instance.author.username} удалил поездку',
        'current_data': now.strftime("%Y-%m-%d %H:%M")
        },
        sender_email=email_list,
        recipient_emails=from_email
    )
    message = msg.build_message()

    # Передаём сообщение в Celery задачу для отправки
    send_email_task.delay(message)
