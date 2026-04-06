from django.urls import path
from . import views

app_name = 'anime'

urlpatterns = [

    path('', views.AnimeListView.as_view(), name='anime_list'),
    path('<int:pk>/', views.AnimeDetailView.as_view(), name='anime_detail'),
    path('genre/<int:genre_id>/', views.AnimeListView.as_view(), name='anime_by_genre'),
    path('year/<int:year>/', views.AnimeListView.as_view(), name='anime_by_year'),
]