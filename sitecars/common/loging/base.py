import logging
import time
from contextlib import contextmanager

from django.db.backends.postgresql.base import DatabaseWrapper as DjangoDatabaseWrapper
from django.db.backends.utils import CursorWrapper as DjangoCursorWrapper

logger = logging.getLogger('duration_request_view')


@contextmanager
def calc_sql_time(sql: str) -> None:
    """
    ����������� �������� ��� ����������� ������� ���������� SQL-�������.

    :param sql: SQL-������, ��� �������� ����� ������������ ����� ����������.
    """
    timestamp = time.monotonic()
    yield

    logger.info(
        f'����������������� SQL-������� {sql} - '
        f'{time.monotonic() - timestamp:.7f} ���.'
    )


class CursorWrapper(DjangoCursorWrapper):
    def execute(self, sql: str, params: list = None) -> None:
        """
            ��������� SQL-������ � �������� ��� �����������������.
        """
        with calc_sql_time(sql):
            return super().execute(sql, params)


class DatabaseWrapper(DjangoDatabaseWrapper):
    """
        ������� ������ ��� ���������� SQL-��������.
    """

    def create_cursor(self, name: str = None) -> CursorWrapper:
        cursor = super().create_cursor(name)
        return CursorWrapper(cursor, self)