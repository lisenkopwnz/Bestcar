from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, request, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from django.contrib import messages

from bestcar.models import Publishing_a_trip
from bestcar.utils import DataMixin
from sitecars import settings

from users.forms import LoginUserForms, UserProfile, User_Password_change_form,Registration_User_Form


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForms
    template_name = 'users/login.html'
    title_page = 'Авторизация'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)




class RegisterUser(CreateView):
    form_class = Registration_User_Form
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


class ProfileUser(DataMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfile
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, default_image=settings.DEFAULT_USER_IMAGE)

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class Users_Password_change(PasswordChangeView):
    form_class = User_Password_change_form
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"


@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return HttpResponseRedirect(reverse('users:register'))


class User_trip(LoginRequiredMixin, DataMixin, ListView):
    context_object_name = 'mein_trip'
    model = Publishing_a_trip
    template_name = 'users/users_trips_current.html'
    title_page = 'Ваши поездки'

    def get_queryset(self):
        try:
            mein_trip = Publishing_a_trip.objects.filter(author=self.request.user)
            return mein_trip
        except Exception as e:  # Обработка всех типов исключений
            return JsonResponse({'error': str(e)}, status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)