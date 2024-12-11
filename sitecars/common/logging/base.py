import logging
import time
from contextlib import contextmanager

from django.db.backends.postgresql.base import DatabaseWrapper as DjangoDatabaseWrapper
from django.db.backends.utils import CursorWrapper as DjangoCursorWrapper

# Ћоггер дл¤ логировани¤ времени выполнени¤ запросов
logger = logging.getLogger('duration_request_view')


@contextmanager
def calc_sql_time(sql: str) -> None:
    """
     онтекстный менеджер дл¤ логировани¤ времени выполнени¤ SQL-запроса.

    :param sql: SQL-запрос, дл¤ которого будет логироватьс¤ врем¤ выполнени¤.
    """
    timestamp = time.monotonic()
    logger.info(f'Ќачало выполнени¤ запроса: {sql}')  # Ћогируем начало выполнени¤ запроса
    yield  # выполнение SQL-запроса
    execution_time = time.monotonic() - timestamp
    logger.info(f'ѕродолжительность SQL-запроса {sql} - {execution_time:.7f} сек.')  # Ћогируем продолжительность


class CursorWrapper(DjangoCursorWrapper):
    def execute(self, sql: str, params: list = None) -> None:
        """
        ¬ыполн¤ет SQL-запрос и логирует его продолжительность.
        """
        with calc_sql_time(sql):  # »спользуем контекстный менеджер дл¤ логировани¤ времени запроса
            return super().execute(sql, params)


class DatabaseWrapper(DjangoDatabaseWrapper):
    """
    —оздает курсор дл¤ выполнени¤ SQL-запросов.
    """

    def create_cursor(self, name: str = None) -> CursorWrapper:
        cursor = super().create_cursor(name)
        return CursorWrapper(cursor, self)