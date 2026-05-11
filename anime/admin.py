from django.contrib import admin
from .models import Anime, Genre, Author, DubStudio

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'anime_type', 'release', 'rating')
    list_filter = ('anime_type', 'genres')
    search_fields = ('title', 'description')
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(DubStudio)