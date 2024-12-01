from PIL import Image
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.core.files.base import ContentFile
from django.forms import ModelForm
from bestcar.models.category import Category

import logging

from users.services.services_images import load_default_image, convert_to_jpeg_if_needed, resize_image

logger = logging.getLogger('duration_request_view')

class LoginUserForms(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))



    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class Regestration_User_Form(UserCreationForm):
    username = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пороль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пороля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'first_name',
                  'last_name', 'email', 'password1', 'password2', 'category','models_auto',]

        labels = {'email': 'E-mail',
                  'first_name': 'Фамилия',
                  'last_name': 'Отчество',
                  }

    widgets = {'email': forms.TextInput(attrs={'class': 'form-input'}),
               'first_name': forms.TextInput(attrs={'class': 'form-input'}),
               'last_name': forms.TextInput(attrs={'class': 'form-input'}),
               }

    def clean(self) -> str:
        """ Переопределяем метод clean для проверки пороля на уникальность """
        cleaned_data = super().clean()

        email = cleaned_data.get('email')

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такая почта уже существует !')
        return cleaned_data

    def clean_photo(self):
        """
        Проверяет и обрабатывает загруженное изображение.
        Преобразует его в формат JPEG, приводит к заданному размеру и обрабатывает ошибку при загрузке.
        Если изображение не загружено, используется изображение по умолчанию.

        :return: Обработанное изображение в формате JPEG и нужного размера.
        :raises ValidationError: Если не удается обработать изображение.
        """
        image = self.cleaned_data.get('photo')

        # Если изображение не загружено, используем изображение по умолчанию
        if not image:
            image = load_default_image()
        try:
            # Открываем изображение через Pillow
            img = Image.open(image)

            # Приводим изображение к одному размеру
            img = resize_image(img, size=(500, 500))

            # Проверяем формат изображения и преобразуем его в JPEG, если нужно
            if img.format != 'JPEG':
                image = convert_to_jpeg_if_needed(img)

        except Exception as e:
            raise forms.ValidationError(f"Не удалось обработать изображение: {e}")

        # Возвращаем обработанное изображение
        return image


class UserProfile(ModelForm):
    username = forms.CharField(disabled=True, label='Имя',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='email',
                            widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name']
        labels = {'email': 'E-mail',
                  'first_name': 'Фамилия',
                  'last_name': 'Отчество',
                  }

        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-input'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-input'}),
                   }


class User_Password_change_form(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пороль',
                                   widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label='Новый пороль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Потверждение пороля',
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))
