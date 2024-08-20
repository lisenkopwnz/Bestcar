from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView, \
    PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from . import views
from .views import LoginUser, RegisterUser, ProfileUser, Users_Password_change, User_trip

app_name = 'users'

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('users_trips_current/', User_trip.as_view(), name='trips_current'),
    path('delete/', views.delete_user, name='delete'),
    path('password-change/', Users_Password_change.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name = 'users/password_change_done.html'),
                                                                 name='password_change_done'),


    path('password-reset/', PasswordResetView.as_view(template_name = 'users/password_reset_form.html',
                                                      email_template_name='users/password_reset_email.html',
                                                      success_url = reverse_lazy('users:password_reset_done')),
                                                      name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'),
                                                                 name='password_reset_done'),


    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html',
                                                                              success_url = reverse_lazy('users:password_reset_complete')),
                                                                 name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'),
                                                                 name='password_reset_complete'),

]
