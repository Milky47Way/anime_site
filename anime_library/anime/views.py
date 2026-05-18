from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Avg, Q
from .models import Anime, Review
from profiles.models import UserAnime


def update_anime_rating(anime):
    avg_score = anime.reviews.aggregate(Avg('rating'))['rating__avg']
    if avg_score is not None:
        anime.rating = round(avg_score, 1)
    else:
        anime.rating = 0.0
    anime.save()
class AnimeListView(ListView):
    model = Anime
    template_name = 'anime/anime_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        # Початковий список аніме
        qs = Anime.objects.all().order_by('-release')
        query = self.request.GET.get('q')
        if query:
            query = query.strip()

            q_lower = query.lower()
            q_cap = query.capitalize()
            q_title = query.title()
            q_upper = query.upper()

            qs = qs.filter(
                Q(title__contains=q_lower) |
                Q(title__contains=q_cap) |
                Q(title__contains=q_title) |
                Q(title__contains=q_upper) |
                Q(genres__name__iexact=query) |
                Q(release__year__icontains=query)
            ).distinct()
        genre_id = self.kwargs.get('genre_id')
        if genre_id:
            qs = qs.filter(genres__id=genre_id)


        year = self.kwargs.get('year')
        if year:
            qs = qs.filter(release__year=year)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_genre'] = self.kwargs.get('genre_id')
        context['selected_year'] = self.kwargs.get('year')
        context['search_query'] = self.request.GET.get('q', '')

        if self.request.user.is_authenticated:
            context['user_watchlist_ids'] = list(
                UserAnime.objects.filter(user=self.request.user).values_list('anime_id', flat=True)
            )
        return context


class AnimeDetailView(DetailView):
    model = Anime
    template_name = 'anime/detail.html'
    context_object_name = 'anime'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        anime = self.object
        context['reviews'] = anime.reviews.all()
        return context

@login_required
def toggle_watchlist(request, anime_id):
    if request.method == 'POST':
        anime_obj = get_object_or_404(Anime, pk=anime_id)
        user_anime, created = UserAnime.objects.get_or_create(
            user=request.user,
            anime=anime_obj,
            defaults={'status': 'PLANNING'}
        )
        if not created:
            user_anime.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect(request.META.get('HTTP_REFERER', 'anime:anime_list'))


@login_required
def add_review(request, anime_id):
    if request.method == 'POST':
        anime_obj = get_object_or_404(Anime, pk=anime_id)
        rating = request.POST.get('rating')
        text = request.POST.get('text')

        if rating and text:
            Review.objects.create(
                anime=anime_obj,
                user=request.user,
                rating=rating,
                text=text
            )
            update_anime_rating(anime_obj)

    return redirect('anime:anime_detail', pk=anime_id)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    anime_id = review.anime.id

    if request.method == 'POST':
        if request.user == review.user or request.user.is_staff:
            rating = request.POST.get('rating')
            text = request.POST.get('text')

            if rating and text:
                review.rating = rating
                review.text = text
                review.save()
                update_anime_rating(review.anime)

    return redirect('anime:anime_detail', pk=anime_id)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    anime_obj = review.anime

    if request.user == review.user or request.user.is_staff:
        review.delete()
        update_anime_rating(anime_obj)

    return redirect('anime:anime_detail', pk=anime_obj.id)