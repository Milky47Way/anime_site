from django.urls import path
from . import views

app_name = 'characters'

# characters/urls.py
urlpatterns = [
    path('<int:pk>/', views.CharacterDetailView.as_view(), name='character_detail'),
    path('<int:pk>/edit/', views.CharacterUpdateView.as_view(), name='character_edit'),
]
