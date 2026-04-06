from django.urls import path
from . import views

app_name = 'characters'

urlpatterns = [
    path('<int:pk>/', views.CharacterDetailView.as_view(), name='character_detail'),
]