from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # НОВЕ ПОЛЕ: Унікальний номер акаунту, який не можна редагувати вручну в адмінці
    account_number = models.IntegerField("Номер акаунту", unique=True, null=True, blank=True, editable=False)

    nickname = models.CharField("Нікнейм", max_length=100, blank=True)
    avatar = models.ImageField("Аватар", upload_to='avatars/', null=True, blank=True)
    bio = models.TextField("Про себе", max_length=500, blank=True)
    birth_date = models.DateField("Дата народження", null=True, blank=True)
    region = models.CharField("Регіон", max_length=100, blank=True, default="Священні землі")

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"

    def __str__(self):
        # Якщо номер уже присвоєно, покажемо його красу в адмінці
        if self.account_number is not None:
            return f"Профіль №{self.account_number} ({self.user.username})"
        return f"Профіль {self.user.username}"

    # Магічна властивість для динамічного підрахунку віку без збереження в БД
    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                        (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

    # ПЕРЕВИЗНАЧАЄМО МЕТОД ЗБЕРЕЖЕННЯ:
    def save(self, *args, **kwargs):
        # Перевіряємо, чи це новий акаунт (у якого ще немає номера)
        if self.account_number is None:
            # Витягуємо з бази набір (set) усіх уже зайнятих номерів для швидкості пошуку
            taken_numbers = set(Profile.objects.values_list('account_number', flat=True))

            number = 0
            # Розумний цикл: починаємо з 0 і крокуємо вгору, поки не знайдемо першу вільну "дірку"
            while number in taken_numbers:
                number += 1

            self.account_number = number

        super().save(*args, **kwargs)


class UserAnime(models.Model):
    STATUS_CHOICES = [
        ('WATCHING', 'Дивлюся'),
        ('WATCHED', 'Переглянуто'),
        ('PLANNING', 'У планах'),
        ('DROPPED', 'Кинуто'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='PLANNING')
    episodes_watched = models.PositiveIntegerField("Переглянуто серій", default=0)
    comment = models.TextField("Мій коментар", blank=True)

    class Meta:
        verbose_name = "Аніме у списку"
        verbose_name_plural = "Списки аніме користувачів"

    def __str__(self):
        return f"{self.user.username} - {self.anime.title}"

    from django.db.models.signals import post_save
    from django.dispatch import receiver
    from django.conf import settings
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.get_or_create(user=instance)
        else:
            if hasattr(instance, 'profile'):
                instance.profile.save()