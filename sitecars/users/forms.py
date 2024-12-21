from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
                                    AuthenticationForm,
                                    PasswordChangeForm,
                                    BaseUserCreationForm
                                    )
from django.forms import ModelForm
from bestcar.models.category import Category
from users.mixins import PhotoProcessingMixin


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


class Registration_User_Form(PhotoProcessingMixin, BaseUserCreationForm):
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


class UserProfile(PhotoProcessingMixin, ModelForm):
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
