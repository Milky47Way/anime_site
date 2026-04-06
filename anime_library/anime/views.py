from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Anime

class AnimeListView(ListView):
    model = Anime
    template_name = 'anime/anime_list.html'
    # Используем object_list, чтобы твой цикл {% for anime in object_list %} заработал сразу
    context_object_name = 'object_list'

    def get_queryset(self):

        qs = Anime.objects.all().order_by('-release')

        # Фильтр поиска (q)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(title__icontains=query)

        # Фильтр по жанру
        genre_id = self.kwargs.get('genre_id')
        if genre_id:
            qs = qs.filter(genres__id=genre_id) # Исправила на genres__id (многие-ко-многим)

        # Фильтр по году
        year = self.kwargs.get('year')
        if year:
            qs = qs.filter(release__year=year)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_genre'] = self.kwargs.get('genre_id')
        context['selected_year'] = self.kwargs.get('year')
        context['search_query'] = self.request.GET.get('q')
        return context


class AnimeDetailView(DetailView):
    model = Anime
    template_name = 'anime/detail.html'
    context_object_name = 'anime'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['characters'] = self.object.characters.all()

        context['reviews'] = self.object.reviews.all()
        return context