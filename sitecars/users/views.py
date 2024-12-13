import logging
from multiprocessing.util import get_logger

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import Prefetch

from django.http import HttpResponseRedirect, JsonResponse

from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from bestcar.models import Publishing_a_trip
from bestcar.utils import DataMixin
from booking.models import Booking


from users.forms import (
                         LoginUserForms,
                         UserProfile,
                         User_Password_change_form,
                         Registration_User_Form
                         )

logger = logging.getLogger('duration_request_view')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForms
    template_name = 'users/login.html'
    title_page = 'Авторизация'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class RegisterUser(DataMixin, CreateView):
    form_class = Registration_User_Form
    template_name = 'users/registration.html'
    title_page = 'Регистрация'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class ProfileUser(DataMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfile
    title_page = 'Профиль'
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class Users_Password_change(PasswordChangeView):
    form_class = User_Password_change_form
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"


class User_trip(LoginRequiredMixin, DataMixin, ListView):
    context_object_name = 'mein_trip'
    template_name = 'users/users_trips_current.html'
    title_page = 'Ваши поездки'

    def get_queryset(self):
        # Используем select_related для подгрузки связанных объектов с использованием FK (например, автор поездки)
        mein_trip = Publishing_a_trip.objects.filter(author=self.request.user).select_related('author')

        # Используем prefetch_related для бронирований и их фотографий, делаем выборку только нужных полей
        mein_trip = mein_trip.prefetch_related(
            Prefetch('bookings',
                     queryset=Booking.objects.select_related('name_companion').only('name_companion__photo'))
        )

        return mein_trip


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return HttpResponseRedirect(reverse('users:register'))


