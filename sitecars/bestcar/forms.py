from django import forms
from django.core.exceptions import ValidationError
from django_currentuser.middleware import get_current_user
from django.contrib.auth import get_user_model

from bestcar.models import Publishing_a_trip

import re

from typing import List, Tuple


class Publishing_a_tripForm(forms.ModelForm):
    free_seating = forms.ChoiceField(
        choices=[],
        label='количество мест'
    )

    @staticmethod
    def seating() -> List[Tuple[int, str]]:
        """Определяем возможные значения 'choices' в поле 'free_seating' """
        current_user_id = get_current_user().id

        category = get_user_model().objects.get(id=current_user_id).category.name
        if category == 'Автомобиль':
            return list(zip((x for x in range(1, 8)), (str(y) for y in range(1, 8))))
        elif category == 'Автобус':
            return list(zip((x for x in range(1, 30)), (str(y) for y in range(1, 30))))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['free_seating'].choices = Publishing_a_tripForm.seating()

    def clean(self):
        """
            Переопределяет метод clean для выполнения проверки логики времени отправления и прибытия.

            Этот метод выполняет проверку, чтобы убедиться, что время отправления (departure_time)
            не может быть больше или равно времени прибытия (arrival_time). Если это условие нарушается,
            генерируется исключение ValidationError с соответствующим сообщением.
        """
        cleaned_data = super().clean()
        if cleaned_data['departure_time'] >= cleaned_data['arrival_time']:
            raise ValidationError('Отправления не может быть раньше прибытия.')
        return cleaned_data


    class Meta:
        model = Publishing_a_trip
        fields = ['departure', 'arrival', 'departure_time',
                  'arrival_time', 'free_seating', 'price']

        labels = {
            'departure': 'Введите место отправление ',
            'arrival': 'Введите место прибытия ',
            'free_seating': 'Количество свободных мест',
            'price': 'Цена поездки'
        }
        widgets = {'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
                   'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
                   }


class Update_form(forms.ModelForm):
    """
        Форма предназначена для внесения изменений в существующие поездки
    """

    class Meta:
        model = Publishing_a_trip
        fields = ['departure', 'arrival',  'departure_time', 'arrival_time']

        labels = {
            'departure': 'Введите место отправления:',
            'arrival': 'Введите место прибытия:',
            'departure_time': 'Введите время отправления:',
            'arrival_time': 'Введите время прибытия:',
        }

        widgets = {'departure_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
                   'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
                   }

    @staticmethod
    def clean_data(data: str) -> str:
        """ Общий метод для валидации вводимых значений ,пользотель имеет право вводить
            только разпешенные символы.
        """
        if re.search(r'[^а-яА-ЯёЁ0-9-,.]', data):
            raise ValidationError('Поле содержит не разрешенные символы')
        else:
            return data

    def clean(self) -> dict:
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

class SearchForm(forms.Form):
    departure = forms.CharField(max_length=200,
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Откуда...'})
                                )
    arrival = forms.CharField(max_length=200,
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Куда...'})
                                )
    seating = forms.IntegerField(min_value=1,
                                 initial=1,
                                 widget=forms.NumberInput(
                                     attrs={'placeholder': 'Введите количество мест'})
                                 )
    datetime = forms.DateTimeField(widget=forms.DateTimeInput(
                                        attrs={'type': 'datetime-local'})
    )
