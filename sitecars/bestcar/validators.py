import logging
from django.utils import timezone
from django.core.exceptions import ValidationError
import inspect

logger = logging.getLogger('duration_request_view')


class ValidatorsDateModel:
    """
    Валидатор для проверки даты. Убедитесь, что введённая дата не меньше текущей.
    """

    def __init__(self, message: str = 'Введите корректную дату.') -> None:
        """
        Инициализация валидатора..
        """
        self.message = message

    def __call__(self, value) -> None:
        """
        Проверяет, является ли переданное значение датой в будущем.
        """
        now = timezone.now()

        if value < now:
            raise ValidationError(self.message)

    def deconstruct(self) -> tuple:
        """
        Возвращает путь для сериализации валидатора.
        """
        path = "%s.%s" % (
            inspect.getmodule(self).__name__,
            self.__class__.__name__,
        )
        return path, (), {}
