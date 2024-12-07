from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from common.celery.utils.decorators import email_address_decorator
from .models.publishing_a_trip import Publishing_a_trip
from common.celery.utils.tasks import send_email_task

from typing import List


@receiver(post_save, sender=Publishing_a_trip)
@email_address_decorator(model=Publishing_a_trip)
def notify_about_change(sender: type,
                        instance: Publishing_a_trip,
                        created: bool,
                        email_list: List[str],
                        **kwargs: dict
                        ) -> None:
    """
    Сигнал, который оповещает пользователей о изменениях в поездке.

    Аргументы:
    sender -- Модель, которая вызвала сигнал.
    instance -- Экземпляр модели, который был сохранен.
    created -- Булево значение, указывающее, был ли создан новый экземпляр.
    email_list -- Список адресов электронной почты для уведомлений.
    **kwargs -- Дополнительные аргументы.
    """
    if not created:
        # получаем текущую дату и время
        now = timezone.now()

        # Генерируем HTML-содержимое письма из шаблона
        html_message = render_to_string('email.html', {
            'information': f'Ваш водитель {instance.author.username} изменил условия поездки',
            'current_data': now.strftime("%Y-%m-%d %H:%M")
        })

        # Удаляем HTML-теги, чтобы получить текстовое содержание
        text_content = strip_tags(html_message)

        # Отправляем задачу на отправку письма с использованием Celery
        send_email_task.delay(
            'Информация об изменении в параметрах поездки',  # Тема письма
            html_message,  # HTML-содержимое письма
            email_list,  # Список получателей
            text_content  # Текстовое содержание письма
        )


@receiver(post_delete, sender=Publishing_a_trip)
@email_address_decorator(model=Publishing_a_trip)
def notify_about_delete(sender: type,
                        instance: Publishing_a_trip,
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
        'information': f'{instance.author.username} удалил поездку',
        'current_data': now.strftime("%Y-%m-%d %H:%M")
    })

    # Удаляем HTML-теги, чтобы получить текстовое содержание
    text_content = strip_tags(html_message)

    send_email_task.delay(
        'Уведомление об удалении поездки',  # Тема письма
        html_message,  # HTML-содержимое письма
        ['zadorojnii260715@icloud.com'],  # Список получателей
        text_content  # Текстовое содержание письма
    )