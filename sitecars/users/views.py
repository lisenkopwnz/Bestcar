import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView

from django.db.models import Prefetch

from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from bestcar.models import Publishing_a_trip
from booking.models import Booking
from common.utils.base_view import BaseView
from common.utils.repository.django_orm_repository import ORMRepository
from bestcar.utils import DataMixin
from users.forms import (
                         LoginUserForms,
                         UserProfile,
                         User_Password_change_form,
                         Registration_User_Form
                        )

logger = logging.getLogger('duration_request_view')


class LoginUser(DataMixin, BaseView, LoginView):
    """Предстовление отвечающее за вход зарегестрированного пользователя в систему"""
    form_class = LoginUserForms
    template_name = 'users/login.html'
    title_page = 'Авторизация'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class RegisterUser(DataMixin, BaseView, CreateView):
    """Предстовление отвечающее за регестрацию пользователя в системе"""
    form_class = Registration_User_Form
    template_name = 'users/registration.html'
    title_page = 'Регистрация'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class ProfileUser(DataMixin, BaseView, LoginRequiredMixin, UpdateView):
    """Предстовление отвечающее за профиль пользователя """
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
    """Предстовление отвечающее за востоновление пороля пользователя в системе"""
    form_class = User_Password_change_form
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"


class User_trip(LoginRequiredMixin, BaseView, DataMixin, ListView):
    """Предстовление отвечающее за отображения списка опубликованных поездок пользователя """
    context_object_name = 'mein_trip'
    template_name = 'users/users_trips_current.html'
    title_page = 'Ваши поездки'
    repository = ORMRepository(Publishing_a_trip)

    def get_queryset(self):
        """Получаем поездки пользователя а также дополнительнуэ информацию о нем"""
        mein_trip = self.repository.filter(author=self.request.user).select_related('author')

        mein_trip = mein_trip.prefetch_related(
            Prefetch('bookings',
                     queryset=Booking.objects.select_related('name_companion').only('name_companion__photo'))
        )
        return mein_trip


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class DeleteUserTrip(BaseView, DeleteView):
    """Предстовление отвечающее за удаление опубликованной поездки пользователя """
    model = Publishing_a_trip
    template_name = 'users/confirmation_deletion.html'
    success_url = reverse_lazy('users:trips_current')

    def post(self, request, *args, **kwargs):
        messages.success(request, "Поездка удалена")
        return super().post(request, *args, **kwargs)


class DeleteUser(BaseView, DeleteView):
    """Предстовление отвечающее за удаление аккаунта пользователя """
    model = get_user_model()
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('users:register')

    def get_object(self, queryset=None):
        return self.request.user
