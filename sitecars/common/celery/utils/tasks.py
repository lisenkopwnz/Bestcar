import logging

from celery import shared_task

from common.utils.services.email_services import EmailMessageBuilder

logger = logging.getLogger('duration_request_view')

@shared_task
def send_email_task(subject, template_name, context, sender_email, recipient_emails):
    """
    Задача Celery для отправки email-сообщений.
    """
    # Создание объекта EmailMultiAlternatives внутри задачи
    msg = EmailMessageBuilder(
        subject=subject,
        template_name=template_name,
        context=context,
        sender_email=sender_email,
        recipient_emails=recipient_emails
    )
    message = msg.build_message()
    message.send()