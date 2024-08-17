from django.utils import timezone

from django.core.exceptions import ValidationError

import inspect

import re


class Validators_date_model:
    def __init__(self, message='Ведите коректную дату.'):
        self.message = message

    def __call__(self, value):
        now = timezone.now()
        if value < now:
            raise ValidationError(self.message)

    def deconstruct(self):
        # Получаем путь к классу
        path = "%s.%s" % (
            inspect.getmodule(self).__name__,
            self.__class__.__name__,
        )
        # Возвращаем кортеж из path, args, kwargs
        return path, (), {}


class Validators_language_model:
    def __init__(self, message='Поле должно содержать только русские символы'):
        self.message = message

    def __call__(self, value):
        if re.search(r'[^а-яА-ЯёЁ]', value):
            raise ValidationError(self.message)

    def deconstruct(self):
        # Получаем путь к классу
        path = "%s.%s" % (
            inspect.getmodule(self).__name__,
            self.__class__.__name__,
        )
        # Возвращаем кортеж из path, args, kwargs
        return path, (), {}
