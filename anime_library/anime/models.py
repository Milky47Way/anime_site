from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Genre(models.Model):
    name = models.CharField("Жанр", max_length=50, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"
        ordering = ['name']

    def __str__(self): return self.name


class Author(models.Model):
    name = models.CharField("Автор", max_length=100)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Автори"

    def __str__(self): return self.name


class DubStudio(models.Model):
    name = models.CharField("Назва студії", max_length=100)
    language = models.CharField("Мова", max_length=100)

    class Meta:
        verbose_name = "Студія дубляжу"
        verbose_name_plural = "Студії дубляжу"

    def __str__(self): return f"{self.name} ({self.language})"


class Anime(models.Model):
    title = models.CharField("Назва", max_length=250)
    poster = models.ImageField("Постер", upload_to='images/posters')
    description = models.TextField("Опис", blank=True)
    age_rating = models.CharField(max_length=15, blank=True, null=True, verbose_name="Віковий рейтинг")
    related_anime = models.ManyToManyField('self', blank=True, verbose_name="Пов'язані тайтли")

    TYPE_CHOICES = [('TV', 'Серіал'), ('MOVIE', 'Фільм'), ('OVA', 'OVA')]
    anime_type = models.CharField("Тип", max_length=10, choices=TYPE_CHOICES, default='TV')
    episodes = models.PositiveIntegerField("Кількість серій", default=0)
    movies_count = models.PositiveIntegerField("Кількість фільмів", default=0)
    ova_count = models.IntegerField(default=0, verbose_name="Кількість OVA")

    genres = models.ManyToManyField(Genre, related_name="anime", verbose_name="Жанри")
    authors = models.ManyToManyField(Author, related_name="anime", verbose_name="Автори")
    dub_studios = models.ManyToManyField(DubStudio, related_name="anime", verbose_name="Студії дубляжу")

    release = models.DateField("Дата релізу")
    trailer_url = models.URLField("Посилання на трейлер", blank=True)
    rating = models.DecimalField(
        "Рейтинг",
        max_digits=3, decimal_places=1, default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )

    class Meta:
        verbose_name = "Аніме"
        verbose_name_plural = "Аніме"
        ordering = ['title']


    def __str__(self): return self.title


class Review(models.Model):
    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField("Відгук")
    rating = models.PositiveIntegerField(
        "Оцінка",
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Поле для вкладених відповідей
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ['-created_at']

    def __str__(self):
        return f"Відгук від {self.user.username} на {self.anime.title}"