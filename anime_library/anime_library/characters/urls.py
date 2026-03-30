from django.urls import path
from .views import CharacterDetailView, CharacterUpdateView

urlpatterns = [
    path('character/<int:pk>/', CharacterDetailView.as_view(), name='character_detail'),
    path('character/<int:pk>/edit/', CharacterUpdateView.as_view(), name='character_edit'),
]
