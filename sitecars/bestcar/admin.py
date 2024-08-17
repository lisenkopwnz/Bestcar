from django.contrib import admin
from .models import Publishing_a_trip,Category


@admin.register(Publishing_a_trip)
class Publishing_a_trip_admin(admin.ModelAdmin):
    # Разделяем форму на две части
    fieldsets = [
        ('Основная информация',{'fields' : ['departure', 'arrival', 'departure_time', 'arrival_time','price']
                                }),

        ('Дополнительная информация', {'fields' : ['seating', 'cat', 'author', 'slug']
                                       })

    ]
    list_display_links = ('id',)
    list_filter = ('departure','arrival','departure_time','arrival_time' ,'cat', 'price', 'seating')
    list_display = ('id', 'departure', 'arrival','models_auto',
                    'departure_time','arrival_time','seating','cat','price','slug')
    ordering = ['departure', 'arrival', 'departure_time']

@admin.register(Category)
class Category_admin(admin.ModelAdmin):
    list_display_links = ('id',)
    list_display = ('id',)

    def get_actions(self, request):  # Убираем возможность удалить поле модели Category через админпанель
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
