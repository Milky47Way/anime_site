from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField("Аватар", upload_to='avatars/', default='avatars/default.png', null=True, blank=True)
    bio = models.TextField("Про себе", max_length=500, blank=True)
    birth_date = models.DateField("Дата народження", null=True, blank=True)
    status_message = models.CharField("Статус", max_length=100, blank=True)
    watchlist = models.ManyToManyField('anime.Anime', blank=True, related_name='watchlisted_by')

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"
    def __str__(self): return f"Профіль {self.user.username}"

class UserAnime(models.Model):
    STATUS_CHOICES = [('watching', 'Дивлюсь'), ('completed', 'Переглянуто'), ('on_hold', 'Відкладено'), ('dropped', 'Кинуто'), ('planned', 'У планах')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_anime_list")
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE, related_name="user_statuses", verbose_name="Аніме")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='planned')
    rating = models.PositiveSmallIntegerField("Особистий рейтинг", validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True)
    episodes_watched = models.PositiveSmallIntegerField("Переглянуто серій", default=0)
    comment = models.TextField("Мій коментар", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Список аніме користувача"
        verbose_name_plural = "Списки аніме користувачів"
        unique_together = ('user', 'anime')
    def __str__(self): return f"{self.user.username} - {self.anime.title}"

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField("Текст відгуку")
    rating = models.PositiveSmallIntegerField("Оцінка", default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ['-created_at']
        unique_together = ('user', 'anime')


class Anime:
    pass