from django.shortcuts import render
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Character

# Детальна сторінка героя
class CharacterDetailView(DetailView):
    model = Character
    template_name = 'characters/detail.html'
    context_object_name = 'character'

    def get_queryset(self):
        # prefetch_related допомагає швидко завантажити ManyToMany зв'язки (родичів)
        return Character.objects.all().prefetch_related('family').select_related('anime')

# сторінка для редагування героя
class CharacterUpdateView(UpdateView):
    model = Character
    fields = ['name', 'age', 'role', 'description', 'family', 'photo']
    template_name = 'characters/edit.html'

    def get_success_url(self): # цей метод переведе назад на сторінку з описом персонажа після редагування
        return reverse_lazy('character_detail', kwargs={'pk': self.object.pk})