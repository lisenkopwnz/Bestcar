import logging
import time
from contextlib import contextmanager

from django.db.backends.postgresql.base import DatabaseWrapper as DjangoDatabaseWrapper
from django.db.backends.utils import CursorWrapper as DjangoCursorWrapper

logger = logging.getLogger('duration_request_view')


@contextmanager
def calc_sql_time(sql: str) -> None:
    """
     онтекстный менеджер дл€ логировани€ времени выполнени€ SQL-запроса.

    :param sql: SQL-запрос, дл€ которого будет логироватьс€ врем€ выполнени€.
    """
    timestamp = time.monotonic()
    yield

    logger.info(
        f'ѕродолжительность SQL-запроса {sql} - '
        f'{time.monotonic() - timestamp:.7f} сек.'
    )


class CursorWrapper(DjangoCursorWrapper):
    def execute(self, sql: str, params: list = None) -> None:
        """
            ¬ыполн€ет SQL-запрос и логирует его продолжительность.
        """
        with calc_sql_time(sql):
            return super().execute(sql, params)


class DatabaseWrapper(DjangoDatabaseWrapper):
    """
        —оздает курсор дл€ выполнени€ SQL-запросов.
    """

    def create_cursor(self, name: str = None) -> CursorWrapper:
        cursor = super().create_cursor(name)
        return CursorWrapper(cursor, self)