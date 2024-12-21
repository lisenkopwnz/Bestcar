import functools
import logging

from bestcar.models import Publishing_a_trip
from booking.models import Booking

from typing import Callable, Type, Any, List

logger = logging.getLogger()


def email_address_decorator(model: Type) -> Callable:

    """
    Декоратор декорирует функцию обработчик сигнала принимает объект модели который используется в сигнале,
    в зависимости от модели получает список email адресов ,котый будет впоследсвии обрабатываться сигналом.

    :param model: Модель, для которой будет извлекаться список адресов электронной почты.

    :return func: Обернутая функция, которая принимает стандартные параметры сигнала.
    """

    model_to_get_email = {
        'Booking': lambda instance: (
            Publishing_a_trip.objects
            .select_related('author')
            .filter(slug=instance.slug)
            .values_list('author__email', flat=True)
        ),
        'Publishing_a_trip': lambda instance: (
            Booking.objects
            .select_related('name_companion')
            .filter(slug=instance.slug)
            .values_list('name_companion__email', flat=True)
        ),
    }

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(sender: Any, instance: Any, created: bool | None = None, **kwargs: Any) -> Any:

            model_name = model.__name__  # Получаем имя модели
            email_logic = model_to_get_email.get(model_name)  # Достаем логику из словаря
            logger.info(email_logic)

            if email_logic is None:
                logging.error(f"Неизвестная модель: {model_name}")
                email_list: List[str] = []
            else:
                email_querySet = email_logic(instance)
                email_list: List[str] = list(email_querySet)

            logging.info(f'{email_list} успешно возвращены')

            match created:
                case None:
                    return func(sender, instance, email_list, **kwargs)
                case _:
                    return func(sender, instance, created, email_list, **kwargs)

        return wrapper

    return decorator
