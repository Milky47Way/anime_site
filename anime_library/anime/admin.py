from django.contrib import admin
from .models import Anime, Genre, Author, DubStudio


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'anime_type', 'episodes', 'movies_count', 'ova_count', 'release', 'rating')

    list_editable = ('rating',)
    list_filter = ('anime_type', 'genres')
    search_fields = ('title', 'description')
    ordering = ('-release',)
    filter_horizontal = ('genres', 'related_anime')
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(DubStudio)
class DubStudioAdmin(admin.ModelAdmin):
    search_fields = ('name',)