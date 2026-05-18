from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, UserAnime
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Додаткова інформація профілю'
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_editable = ('email',)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'nickname', 'birth_date')
    search_fields = ('user__username', 'nickname', 'user__email')
    readonly_fields = ('get_email',)
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Електронна пошта'

@admin.register(UserAnime)
class UserAnimeAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'status', 'episodes_watched')
    list_filter = ('status',)