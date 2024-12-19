from typing import List
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailMessageBuilder:
    """
    ����� ��� ���������� email-��������� � ��������� � HTML ��������.
    ������������ ��� ��������� �������� �������� � �������� �����.
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
        �������������� ������ EmailMessageBuilder.

        :param subject: ���� ������
        :param template_name: ��� ������� ��� ����������
        :param context: �������� ��� ���������� �������
        :param sender_email: ������ email-������� ������������
        :param recipient_emails: ������ email-������� �����������
        """
        self.subject = subject
        self.template_name = template_name
        self.context = context
        self.from_email = sender_email
        self.to = recipient_emails

    def _render_html_message(self) -> str:
        """
        �������� HTML-��������� �� ������ ������� � ���������.

        :return: �������������� HTML-���������.
        """
        return render_to_string(self.template_name, self.context)

    def _strip_html_tags(self) -> str:
        """
        ������� HTML-���� �� HTML-��������� ��� ��������� ��������� ������.

        :return: ��������� ��������� ��� HTML-�����.
        """
        return strip_tags(self._render_html_message())

    def build_message(self) -> EmailMultiAlternatives:
        """
        ������� � ���������� ������ EmailMultiAlternatives ��� �������� email.

        :return: ������ EmailMultiAlternatives � ��������� � HTML ��������.
        """

        msg = EmailMultiAlternatives(
            self.subject,
            self._strip_html_tags(),
            self.from_email,
            self.to
        )
        msg.attach_alternative(self._render_html_message(), "text/html")
        return msg