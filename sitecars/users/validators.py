import re
from django.core.exceptions import ValidationError
import inspect


class NumberPhoneValidator:
    """
    Валидатор номера телефона.
    Проверяет, что номер телефона начинается с '+7' и содержит ровно 10 цифр после кода страны.
    """

    def __init__(self, message: str = 'Номер телефона должен начинаться с +7 и содержать 10 цифр.') -> None:
        self.message = message

    def __call__(self, value: str) -> None:
        """
        Проверяет корректность значения.
        """
        if not re.match(r'^\+7\d{10}$', str(value)):
            raise ValidationError(self.message)

    def deconstruct(self) -> tuple:
        """
        Возвращает данные для сериализации валидатора.
        """
        path = "%s.%s" % (
            inspect.getmodule(self).__name__,
            self.__class__.__name__,
        )
        return path, (), {}
