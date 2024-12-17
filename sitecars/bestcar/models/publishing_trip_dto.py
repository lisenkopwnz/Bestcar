from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class TripDTO:
    photo: str
    departure: str
    arrival: str
    departure_time: str
    arrival_time: str
    price: str
    category_name: str
    models_auto: str
    username: str
    slug: str
    free_seating: int

    @staticmethod
    def get_author_data(data: Dict[str, Any]) -> Dict[str, Any]:
        return data.get('author', {})

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TripDTO':
        """
        Преобразует словарь данных в объект TripDTO.

            :param data: Словарь данных поездки.
            :return: Объект TripDTO.
        """
        author_data = TripDTO.get_author_data(data)

        return TripDTO(
            departure=data.get('departure'),
            arrival=data.get('arrival'),
            departure_time=data.get('departure_time'),
            arrival_time=data.get('arrival_time'),
            free_seating=data.get('free_seating'),
            price=data.get('price'),
            slug=data.get('slug'),
            username=author_data.get('username'),
            category_name=author_data.get('category_name'),
            photo=author_data.get('photo'),
            models_auto=author_data.get('models_auto'),
        )