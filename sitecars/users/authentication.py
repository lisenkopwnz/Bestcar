from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from typing import Optional


class AuthenticationUserBackend(BaseBackend):
    """
    Кастомный бекенд для аутентификации пользователей по email или номеру телефона.
    """

    def authenticate(self,
                     request: HttpRequest,
                     username: str = None,
                     password: str = None,
                     **kwargs) -> Optional[object]:
        """
        Аутентификация пользователя по email или номеру телефона.

        Аргументы:
            request (HttpRequest): Объект запроса.
            username (str): Email или номер телефона пользователя.
            password (str): Пароль пользователя.

        Возвращает:
            Optional[User]: Аутентифицированный пользователь, если данные верны, или None, если аутентификация не удалась.
        """
        user_model = get_user_model()

        # Попытка найти пользователя по email
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            # Если не найдено по email, пытаемся найти по номеру телефона
            try:
                user = user_model.objects.get(phone_number=username)
            except user_model.DoesNotExist:
                return None

        # Проверка пароля
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id: int) -> Optional[object]:
        """
        Получить пользователя по его ID.

        Аргументы:
            user_id (int): Идентификатор пользователя.

        Возвращает:
            Optional[User]: Пользователь, если найден, или None, если не найден.
        """
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None