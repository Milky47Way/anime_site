from django.urls import path
from .views import AnimeListView, AnimeDetailView

urlpatterns = [
    path('anime/', AnimeListView.as_view(), name='anime_list'),
    path('anime/<int:pk>/', AnimeDetailView.as_view(), name='anime_detail'),
    path('anime/genre/<int:genre_id>/', AnimeListView.as_view(), name='anime_by_genre'),
    path('anime/year/<int:year>/', AnimeListView.as_view(), name='anime_by_year'),
]
