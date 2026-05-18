from django.urls import path

app_name = 'anime'

urlpatterns = [
    path('', views.AnimeListView.as_view(), name='anime_list'),
    path('<int:pk>/', views.AnimeDetailView.as_view(), name='anime_detail'),
    path('genre/<int:genre_id>/', views.AnimeListView.as_view(), name='anime_by_genre'),
    path('year/<int:year>/', views.AnimeListView.as_view(), name='anime_by_year'),
    path('type/<str:anime_type>/', views.AnimeListView.as_view(), name='anime_by_type'),

    path('<int:anime_id>/review/', views.add_review, name='add_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),

    path('toggle-watchlist/<int:anime_id>/', views.toggle_watchlist, name='toggle_watchlist'),
]