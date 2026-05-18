from django.contrib import admin
from .models import Character
from django.contrib import admin
from .models import Character

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'anime', 'role', 'age', 'birthday')
    search_fields = ('name', 'description')
    list_filter = ('anime', 'role')
    filter_horizontal = ('family',)