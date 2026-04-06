from django.contrib import admin
from .models import Profile, UserAnime, Review

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'status_message')
    search_fields = ('user__username', 'status_message')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('text', 'user__username', 'anime__title')

admin.site.register(UserAnime)