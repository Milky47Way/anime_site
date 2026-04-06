from django.contrib import admin
from .models import Character

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'anime')
    list_filter = ('role', 'anime')
    search_fields = ('name',)