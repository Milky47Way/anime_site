from django.views.generic import DetailView
from .models import Profile, UserAnime  # Імпортуємо все з твого models.py


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'  # Краще тримати в папці profiles
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        # 1. Отримуємо стандартний контекст (сам профіль)
        context = super().get_context_data(**kwargs)

        # 2. Додаємо список аніме саме цього користувача
        # self.object — це і є той профіль, який ми зараз відкрили
        context['user_anime_list'] = UserAnime.objects.filter(user=self.object.user)

        return context