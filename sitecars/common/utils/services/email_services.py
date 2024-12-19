from typing import List
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailMessageBuilder:
    """
    Класс для построения email-сообщений с текстовой и HTML версиями.
    Используется для упрощения процесса создания и отправки писем.
    """

    def __init__(
        self,
        subject: str,
        template_name: str,
        context: dict,
        sender_email: List[str],
        recipient_emails: List[str]
    ) -> None:
        """
        Инициализирует объект EmailMessageBuilder.

        :param subject: Тема письма
        :param template_name: Имя шаблона для рендеринга
        :param context: Контекст для рендеринга шаблона
        :param sender_email: Список email-адресов отправителей
        :param recipient_emails: Список email-адресов получателей
        """
        self.subject = subject
        self.template_name = template_name
        self.context = context
        self.from_email = sender_email
        self.to = recipient_emails

    def _render_html_message(self) -> str:
        """
        Рендерит HTML-сообщение на основе шаблона и контекста.

        :return: Сформированное HTML-сообщение.
        """
        return render_to_string(self.template_name, self.context)

    def _strip_html_tags(self) -> str:
        """
        Удаляет HTML-теги из HTML-сообщения для получения текстовой версии.

        :return: Текстовое сообщение без HTML-тегов.
        """
        return strip_tags(self._render_html_message())

    def build_message(self) -> EmailMultiAlternatives:
        """
        Создает и возвращает объект EmailMultiAlternatives для отправки email.

        :return: Объект EmailMultiAlternatives с текстовой и HTML версиями.
        """

        msg = EmailMultiAlternatives(
            self.subject,
            self._strip_html_tags(),
            self.from_email,
            self.to
        )
        msg.attach_alternative(self._render_html_message(), "text/html")
        return msg