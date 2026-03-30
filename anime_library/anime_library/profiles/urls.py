from django.urls import path
from .views import ProfileDetailView
app_name = 'user'

urlpatterns = [
    path('profile/<int:profile_id>/', ProfileDetailView.as_view(), name='profile_detail'),
    ]

