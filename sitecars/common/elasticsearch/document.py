from django_elasticsearch_dsl import Document, fields
from  django_elasticsearch_dsl.registries import registry

from bestcar.models import Publishing_a_trip


@registry.register_document
class PublishingTripDocument(Document):
    departure = fields.TextField(attr='departure')
    arrival = fields.TextField(attr='arrival')
    departure_time = fields.DateField(attr='departure_time')
    arrival_time = fields.DateField(attr='arrival_time')
    free_seating = fields.IntegerField(attr='free_seating')
    reserved_seats = fields.IntegerField(attr='reserved_seats')
    price = fields.IntegerField(attr='price')
    slug = fields.KeywordField(attr='slug')
    author = fields.ObjectField(properties={
        'username': fields.KeywordField(attr='username', index=False),
        'category_name': fields.KeywordField(attr='category.name'),
        'photo.url': fields.KeywordField(attr='photo.url', index=False),
        'models_auto': fields.KeywordField(attr='models_auto', index=False)
    })

    class Index:
        name = 'trip_document'  #Имя индекса Elasticsearch
        settings = {
            'number_of_shards': 1,  #Настройки индекса
            'number_of_replicas': 0
        }

    class Django:
        model = Publishing_a_trip  #Связанная Django модель