from django.shortcuts import render
from bestcar.utils import DataMixin

from django.http import HttpResponse, HttpResponseNotFound, request, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from bestcar.models import Publishing_a_trip, Publishing_a_tripForm
from bestcar.models import *
from sitecars import settings

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from django.urls import reverse_lazy

from .services import TripFilterService


class HommeBestcar(DataMixin, TemplateView):
    model = Publishing_a_trip
    template_name = 'bestcar/index.html'
    title_page = 'Главная страница'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class Bus_trip(DataMixin, ListView):
    model = Publishing_a_trip
    template_name = 'bestcar/bus_trip.html'
    title_page = 'На автобусе'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class Car_trip(DataMixin, ListView):
    model = Publishing_a_trip
    template_name = 'bestcar/car_trip.html'
    title_page = 'На машине'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class SearchTrip(DataMixin, ListView):
    context_object_name = 'search_trip_result'
    template_name = 'bestcar/search.html'
    title_page = 'Поиск'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, default_image=settings.DEFAULT_USER_IMAGE)

    def get_queryset(self):
        departure = self.request.GET.get('d')
        arrival = self.request.GET.get('a')
        seating = self.request.GET.get('s')
        data = self.request.GET.get('t')
        cat = self.request.GET.get('cat')

        return TripFilterService.filter_trip(cat, departure, arrival, seating, data)


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


class Bookings(DataMixin, ListView):
    model = Publishing_a_trip
    template_name = 'bestcar/to_book_a_trip.html'
    title_page = 'FFF'

    def dispatch(self, request, *args, **kwargs):
        self.trip_slug = kwargs.get('trip_slug')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        object_list = queryset.filter(slug=self.trip_slug).first()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, default_image=settings.DEFAULT_USER_IMAGE)


class Checkout(DataMixin, DetailView):
    model = Publishing_a_trip
    template_name = 'bestcar/booking_checkout.html'
    title_page = 'аааа'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, default_image=settings.DEFAULT_USER_IMAGE)





def page_not_found(request, exception):
    return HttpResponseNotFound("<h>Упс ,что пошло не так</h>")


class About(DataMixin, TemplateView):
    template_name = 'bestcar/about.html'
    title_page = 'О сайте'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)
