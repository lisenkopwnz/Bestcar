from PIL import Image
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import (
                                    AuthenticationForm,
                                    PasswordChangeForm,
                                    BaseUserCreationForm
                                    )
from django.forms import ModelForm
from bestcar.models.category import Category
from users.services.services_images import (
                                        load_default_image,
                                        convert_to_jpeg_if_needed,
                                        resize_image
                                        )


class LoginUserForms(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input', 'id': 'username-input'})
                               )
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input','id': 'password1-input'})
                               )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class Registration_User_Form(BaseUserCreationForm):
    username = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-input', 'id': 'username-input'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'id': 'password1-input'})
    )
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'id': 'password2-input'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        initial=Category.objects.first(),
        widget=forms.Select(attrs={'class': 'form-input', 'id': 'category-input'})
    )

    class Meta:
        model = get_user_model()
        fields = [
            'photo',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password1',
            'password2',
            'category',
            'models_auto',
        ]
        labels = {
            'email': 'E-mail',
            'first_name': 'Фамилия',
            'last_name': 'Отчество',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input', 'id': 'email-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'id': 'first-name-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'id': 'last-name-input'}),
        }
        error_messages = {
            'email': {
                'required': 'Адрес электронной почты обязателен для ввода!',
                'unique': 'Этот адрес электронной почты уже используется!',
            },
            'phone_number': {
                'required': 'Номер телефона обязателен для ввода!',
                'unique': 'Этот номер телефона уже зарегистрирован!',
            },
        }


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
            img = resize_image(img, size=(200, 300))

            # Проверяем формат изображения и преобразуем его в JPEG, если нужно
            if img.format != 'JPEG':
                image = convert_to_jpeg_if_needed(img)

        except Exception as e:
            raise forms.ValidationError(f"Не удалось обработать изображение: {e}")

        # Возвращаем обработанное изображение
        return image


class UserProfile(ModelForm):
    username = forms.CharField(label='Имя',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='email',
                            widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = [
            'photo',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'category',
            'models_auto'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class User_Password_change_form(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пороль',
                                   widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label='Новый пороль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Потверждение пороля',
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))
