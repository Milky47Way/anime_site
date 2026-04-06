from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Anime, Review

class AnimeListView(ListView):
    model = Anime
    template_name = 'anime/anime_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        # Початковий список аніме
        qs = Anime.objects.all().order_by('-release')

        # 1. Пошук (Назва, Жанр або Рік)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(genres__name__icontains=query) |
                Q(release__year__icontains=query)
            ).distinct()

        # 2. Фільтрація за ID жанру (з URL)
        genre_id = self.kwargs.get('genre_id')
        if genre_id:
            qs = qs.filter(genres__id=genre_id)

        # 3. Фільтрація за роком (з URL)
        year = self.kwargs.get('year')
        if year:
            qs = qs.filter(release__year=year)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_genre'] = self.kwargs.get('genre_id')
        context['selected_year'] = self.kwargs.get('year')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class AnimeDetailView(DetailView):
    """Цей клас якраз і зник минулого разу! Повертаємо його на місце."""
    model = Anime
    template_name = 'anime/detail.html'
    context_object_name = 'anime'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['characters'] = self.object.characters.all()
        context['reviews'] = self.object.reviews.all().order_by('-created_at')
        return context

def add_review(request, anime_id):
    if request.method == "POST" and request.user.is_authenticated:
        anime = get_object_or_404(Anime, id=anime_id)
        Review.objects.create(
            anime=anime,
            user=request.user,
            text=request.POST.get('text'),
            rating=request.POST.get('rating')
        )
    return redirect('anime:anime_detail', pk=anime_id)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user or request.user.is_staff:
        anime_id = review.anime.id
        review.delete()
        return redirect('anime:anime_detail', pk=anime_id)
    return redirect('anime:anime_list')