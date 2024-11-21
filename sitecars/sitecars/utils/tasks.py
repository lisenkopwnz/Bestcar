import logging
from typing import List

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@shared_task
def send_email_task(subject: str,
                    html_message: str,
                    recipient_list: List[str],
                    text_content: str
                    ):
    """

    :param subject : Тема письма
    :param html_message: html версия тела сообщения
    :param recipient_list: Список email адресов получателей
    :param text_content: Строковая версия сообщения
    :return: None
    """

    # Определяем адреса отправителя и получателя
    from_email = settings.EMAIL_HOST_USER
    to = recipient_list

    # Создаем объект EmailMultiAlternatives
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)

    # Присоединяем HTML-версию сообщения
    msg.attach_alternative(html_message, "text/html")
    logging.info(f'сообщение для пользователей {recipient_list} готовится к отправке')
    # Отправляем сообщение
    msg.send()
