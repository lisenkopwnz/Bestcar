import time
import logging

# Логгер для логирования продолжительности запросов
logger = logging.getLogger('duration_request_view')

class LoggingMiddleware:
    """Middleware для логирования продолжительности запросов и ответов в приложениях."""

    def __init__(self, get_response: callable):
        """
        Инициализация middleware.

        :param get_response: Функция для обработки HTTP-запросов.
        """
        self._get_response = get_response

    def __call__(self, request):
        """
        Обработка входящего запроса.

        :param request: HTTP-запрос.
        :return: HTTP-ответ.
        """
        # Засекаем время начала обработки запроса
        timestamp = time.monotonic()

        # Получаем ответ от view
        response = self._get_response(request)

        # Логируем продолжительность запроса
        logger.info(
            'Продолжительность запроса {request_path} - {result:.7f} сек.'.format(
                request_path=request.path,  # Исправлено: использован request.path, а не request.patch
                result=time.monotonic() - timestamp
            )
        )

        return response