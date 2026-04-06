from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Character

class CharacterDetailView(DetailView):
    model = Character
    template_name = 'characters/detail.html'
    context_object_name = 'character'

    def get_queryset(self):
        return Character.objects.all().prefetch_related('family').select_related('anime')


class CharacterUpdateView(UpdateView):
    model = Character
    fields = ['name', 'age', 'role', 'description', 'family', 'photo']
    template_name = 'characters/edit.html'

    def get_success_url(self):
        return reverse_lazy('characters:character_detail', kwargs={'pk': self.object.pk})