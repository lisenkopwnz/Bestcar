import logging
from datetime import datetime

from django.utils import timezone
import pytz


from bestcar.utils import DataMixin
from bestcar.models import *
from bestcar.forms import Update_form, Publishing_a_tripForm, SearchForm
from common.elasticsearch.document import PublishingTripDocument
from .services import TripFilterService, User_trip_object, elasticsearch_formatting_date

from sitecars import settings

from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, Http404, JsonResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin


logger = logging.getLogger(__name__)


class BaseView(View):
    """ Базовый класс который отлавливает все исклюяения ,которые
        не были обработаны ранее """

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return self._response(e, status=400)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=200):
        """Форматируем HTTP ответ с описание ошибки или формируем JSON ответ в случае необходимости """
        if status != 200:
            res = JsonResponse({
                "errorMessage": str(data),
                "status": status
            })
        else:
            res = JsonResponse({
                "data": str(data),
                "status": status
            })
        return res


class HomeBestcar(DataMixin, TemplateView):
    form_class = SearchForm
    model = Publishing_a_trip
    template_name = 'bestcar/index.html'
    title_page = 'Главная страница'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return self.get_mixin_context(context)


class Bus_trip(DataMixin, ListView):
    form_class = SearchForm
    model = Publishing_a_trip
    template_name = 'bestcar/bus_trip.html'
    title_page = 'На автобусе'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return self.get_mixin_context(context)


class Car_trip(DataMixin, ListView):
    form_class = SearchForm
    model = Publishing_a_trip
    template_name = 'bestcar/car_trip.html'
    title_page = 'На машине'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return self.get_mixin_context(context)


class SearchTrip(DataMixin, ListView):
    context_object_name = 'search_trip_result'
    template_name = 'bestcar/search.html'
    title_page = 'Поиск'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, default_image=settings.DEFAULT_USER_IMAGE)

    def get_data_request(self,form):
        if form.is_valid():
            # Данные формы
            departure = form.cleaned_data['departure']
            arrival = form.cleaned_data['arrival']
            seating = form.cleaned_data['seating']
            datetime_value = form.cleaned_data['datetime']

            # Получаем значение скрытого поля из GET-запроса
            cat = self.request.GET.get('cat')
            return {
                'departure':departure,
                'arrival': arrival,
                'seating': seating,
                'datetime_value': datetime_value,
                'cat':cat
            }

    def get_queryset(self):

        # Создаем экземпляр формы
        form = SearchForm(self.request.GET)

        # Получаем данные из формы
        data = self.get_data_request(form)

        queryset = PublishingTripDocument.search().filter(
            'range', departure_time={'gte': elasticsearch_formatting_date(timezone.now())}
        )
        return queryset



        #return TripFilterService.filter_trip(cat, departure, arrival, free_seating, data)


class Post(DataMixin, LoginRequiredMixin, CreateView):
    form_class = Publishing_a_tripForm
    template_name = 'bestcar/post.html'
    success_url = reverse_lazy('home')
    title_page = 'Опубликовать поездку'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class Update_user_trip(DataMixin, BaseView, UpdateView):
    """
        Представление для извенения параметров поездки
    """
    model = Publishing_a_trip
    form_class = Update_form
    template_name = 'bestcar/update.html'
    success_url = reverse_lazy('home')
    title_page = 'Форма для изменения данных поездки'

    def get(self, request, *args, **kwargs):
        try:
            slug = kwargs['slug']
            User_trip_object.users_trip_object(slug)
            logger.info('запись успешно найдена')
            return super().get(self, request, *args, **kwargs)
        except Http404 as e:
            logger.error(f'произошла ошибка {e}')
            return JsonResponse({
                "errorMessage": str(e),
                "status": 400
            })

    def form_valid(self, form):
        # здесь нужно дабавить отправку сигнала ввиде сообщения об изменениях в поездке
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h>Упс ,что пошло не так</h>")


class About(DataMixin, TemplateView):
    template_name = 'bestcar/about.html'
    title_page = 'О сайте'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)
