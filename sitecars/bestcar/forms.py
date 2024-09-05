from django import forms
from django.core.exceptions import ValidationError

from bestcar.models import Publishing_a_trip

import re


class Update_form(forms.ModelForm):
    """
        Форма предназначена для внесения изменений в существующие поездки
    """

    class Meta:
        model = Publishing_a_trip
        fields = ['departure', 'arrival', 'models_auto', 'departure_time', 'arrival_time']

        labels = {
            'departure': 'Введите место отправление ',
            'arrival': 'Введите место прибытия '
        }

        widgets = {'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
                   'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
                   }

    @staticmethod
    def clean_data(data):
        """ Общий метод для валидации вводимых значений ,пользотель имеет право вводить
            только разпешенные символы.
        """
        if re.search(r'[^а-яА-ЯёЁ0-9-,.]', data):
            raise ValidationError('Поле содержит не разрешенные символы')
        else:
            return data

    def clean(self):
        """
            Переопределяем метод для внесения дополнительной логики валидации полей формы

        """
        cleaned_data = super().clean()
        for field_name in ['departure', 'arrival']:
            value = cleaned_data.get(field_name)
            if value:
                try:
                    self.clean_data(value)
                except ValidationError as e:
                    cleaned_data[field_name] = None
                    self.add_error(field_name, str(e))
        return cleaned_data
