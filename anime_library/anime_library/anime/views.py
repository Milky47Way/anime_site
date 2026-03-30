from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Anime

template_name = "anime/index.html"
context_object_name = "anime"
queryset = Anime.objects.order_by('-release')

class AnimeListView(ListView):
    model = Anime
    template_name = 'anime/index.html'
    context_object_name = 'anime'

    def get_queryset(self):
        qs = Anime.objects.all().order_by('-release')

        # 🔍 пошук
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(title__icontains=query)

        # 🎭 фільтр по жанру
        genre_id = self.kwargs.get('genre_id')
        if genre_id:
            qs = qs.filter(genre_id=genre_id)

        # 📅 фільтр по року
        year = self.kwargs.get('year')
        if year:
            qs = qs.filter(release__year=year)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # додаємо в шаблон (не обов’язково, але зручно)
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
            # Отримуємо персонажів, пов'язаних з цим аніме
            # (related_name='characters' ми вказували в моделі Character)
        context['characters'] = self.object.characters.all()

            # Отримуємо відгуки (якщо модель Review в іншому додатку,
            # переконайся, що в моделі вказано related_name='reviews')
        context['reviews'] = self.object.reviews.all()
