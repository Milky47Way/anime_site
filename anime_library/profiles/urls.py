from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'profiles'

urlpatterns = [
    path('<int:pk>/', views.profile_detail, name='profile_detail'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('my-list/', views.my_list, name='my_list'),
    path('settings/', views.profile_settings, name='profile_settings'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('register/', views.register, name='register'),

path('password-reset/',
     auth_views.PasswordResetView.as_view(template_name='registration/password/password_reset.html'),
     name='password_reset'),

path('password-reset/done/',
     auth_views.PasswordResetDoneView.as_view(template_name='registration/password/password_reset_done.html'),
     name='password_reset_done'),

path('password-reset-confirm/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name='registration/password/password_reset_confirm.html'),
     name='password_reset_confirm'),

path('password-reset-complete/',
     auth_views.PasswordResetCompleteView.as_view(template_name='registration/password/password_reset_complete.html'),
     name='password_reset_complete'),
]