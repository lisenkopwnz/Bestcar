import re

from django.core.exceptions import ValidationError

import inspect


class Validators_date_model:
    def __init__(self, message='����� �������� ������ ���������� � +7 � ��������� 10 ����.'):
        self.message = message

    def __call__(self, value):
        if not re.match(r'^\+7\d{10}$', str(value)):
            raise ValidationError(self.message)


    def deconstruct(self):
        path = "%s.%s" % (
            inspect.getmodule(self).__name__,
            self.__class__.__name__,
        )
        return path, (), {}