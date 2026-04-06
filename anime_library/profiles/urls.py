from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('settings/', views.ProfileUpdateView.as_view(), name='profile_settings'),
    path('<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('my-list/', views.WatchlistView.as_view(), name='my_list'),
    path('toggle-list/<int:pk>/', views.toggle_watchlist, name='toggle_watchlist'),
]