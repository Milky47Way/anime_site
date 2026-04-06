from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView
from .models import Profile, UserAnime, Anime
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'profiles'


# 1. Сторінка "Мій список"
class WatchlistView(LoginRequiredMixin, ListView):
    template_name = 'anime/anime_list.html'  # Використовуємо твій скляний дизайн
    context_object_name = 'object_list'

    def get_queryset(self):

        return self.request.user.profile.watchlist.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Список збереженого'
        return context

@login_required
def toggle_watchlist(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    profile = request.user.profile

    if anime in profile.watchlist.all():
        profile.watchlist.remove(anime)
    else:
        profile.watchlist.add(anime)


    return redirect(request.META.get('HTTP_REFERER', '/'))

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profiles/settings.html'

    fields = ['avatar', 'bio', 'birth_date', 'status_message']
    success_url = reverse_lazy('user:profile_detail')

    def get_object(self):
        return self.request.user.profile
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anime_list'] = UserAnime.objects.filter(user=self.object.user)
        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        user_anime_items = UserAnime.objects.filter(user=self.object.user)

        for item in user_anime_items:
            status = request.POST.get(f'status_{item.id}')
            episodes = request.POST.get(f'episodes_{item.id}')
            comment = request.POST.get(f'comment_{item.id}')

            if status: item.status = status
            if episodes: item.episodes_watched = episodes
            if comment: item.comment = comment
            item.save()

        return redirect('user:profile_detail', pk=self.object.pk)

