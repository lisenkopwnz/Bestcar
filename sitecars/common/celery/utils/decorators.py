import functools
import logging

from bestcar.models import Publishing_a_trip
from booking.models import Booking

from typing import Callable, Type, Any, List

logger = logging.getLogger(__name__)


def email_address_decorator(model: Type[Booking] | Type[Publishing_a_trip]) -> Callable:

    """
    Декоратор декорирует функцию обработчик сигнала принимает объект модели который используется в сигнале,
    в зависимости от модели получает список email адресов ,котый будет впоследсвии обрабатываться сигналом.

    :param model: Модель, для которой будет извлекаться список адресов электронной почты.

    :return func: Обернутая функция, которая принимает стандартные параметры сигнала.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(sender: Any, instance: Any, created: bool | None = None, **kwargs: Any) -> Any:

            email_querySet = None

            if model == Booking:
                email_querySet = (
                    Booking.objects
                    .select_related('name_companion')
                    .filter(trip__slug=instance.trip.slug)
                    .values_list('name_companion__email', flat=True)
                )

            if model == Publishing_a_trip:
                email_querySet = (
                    Publishing_a_trip.objects
                    .select_related('author')
                    .filter(slug=instance.slug)
                    .values_list('author__email', flat=True)
                )

            if email_querySet is None:
                logging.error(f"Неизвестная модель: {model}")

            # Преобразуем QuerySet в список
            email_list: List[str] = list(email_querySet) if email_querySet else []
            logging.info(f'{email_list} успешно возвращены')

            match created:
                case None:
                    return func(sender, instance, email_list, **kwargs)
                case _:
                    return func(sender, instance, created, email_list, **kwargs)

        return wrapper

    return decorator
