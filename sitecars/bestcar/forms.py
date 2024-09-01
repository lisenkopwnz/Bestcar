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

    def clean_departure(self):
        return self.clean_data(self.cleaned_data['departure'])

    def clean_arrival(self):
        return self.clean_data(self.cleaned_data['arrival'])
