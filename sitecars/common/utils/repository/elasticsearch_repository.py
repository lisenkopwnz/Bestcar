from typing_extensions import Type

from common.elasticsearch.document import PublishingTripDocument
from common.utils.interface.interface import StorageRepository


class ELASTRepository(StorageRepository):
    """
        Универсальный репозиторий для работы с документами Elasticsearch.
        При необходимости данный класс может быть расширен доп. методами
    """

    def __init__(self, document: Type[PublishingTripDocument]) -> None:
        self.document = document