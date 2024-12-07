from typing import List

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from booking.models import Booking
from common.celery.utils.decorators import email_address_decorator
from common.celery.utils.tasks import send_email_task


@receiver(post_save, sender=Booking)
@email_address_decorator(model=Booking)
def notify_about_delete(sender: type,
                        instance: Booking,
                        created: bool,
                        email_list: List[str],
                        **kwargs: dict
                        ) -> None:
    """
      Сигнал, который оповещает автора поездки о новом попутчике.

      Аргументы:
      sender -- Модель, которая вызвала сигнал.
      instance -- Экземпляр модели, который был сохранен.
      created -- Булево значение, указывающее, был ли создан новый экземпляр.
      email_list -- Список адресов электронной почты для уведомлений.
      **kwargs -- Дополнительные аргументы.
    """
    if created:
        # получаем текущую дату и время
        now = timezone.now()

        # Генерируем HTML-содержимое письма из шаблона
        html_message = render_to_string('email.html', {
            'information': f'{instance.name_companion.username} вашь новый попутчик',
            'current_data': now.strftime("%Y-%m-%d %H:%M")
        })

        # Удаляем HTML-теги, чтобы получить текстовое содержание
        text_content = strip_tags(html_message)

        # Отправляем задачу на отправку письма с использованием Celery
        send_email_task.delay(
            'Информация о новом попутчике',  # Тема письма
            html_message,  # HTML-содержимое письма
            email_list,  # Список получателей
            text_content  # Текстовое содержание письма
        )


@receiver(post_delete, sender=Booking)
@email_address_decorator(model=Booking)
def notify_about_delete(sender: type,
                        instance: Booking,
                        email_list: List[str],
                        **kwargs: dict
                        ) -> None:
    """ Сигнал который оповещает пользовотелей забронировавших поездку об удалении
        поездки автором роздки.

    Аргументы:
    sender -- Модель, которая вызвала сигнал.
    instance -- Экземпляр модели, который был сохранен.
    email_list -- Список адресов электронной почты для уведомлений.
    **kwargs -- Дополнительные аргументы.
    """

    # получаем текущую дату и время
    now = timezone.now()

    # Генерируем HTML-содержимое письма из шаблона
    html_message = render_to_string('email.html', {
        'information': f'{instance.name_companion.username} больше не ваш попутчик',
        'current_data': now.strftime("%Y-%m-%d %H:%M")
    })

    # Удаляем HTML-теги, чтобы получить текстовое содержание
    text_content = strip_tags(html_message)

    send_email_task.delay(
        'Уведомление об удалении брони',  # Тема письма
        html_message,  # HTML-содержимое письма
        email_list,  # Список получателей
        text_content  # Текстовое содержание письма
    )
