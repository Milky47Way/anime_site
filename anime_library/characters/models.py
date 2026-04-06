from django.db import models

class Character(models.Model):
    name = models.CharField("Ім'я", max_length=250)
    age = models.PositiveSmallIntegerField("Вік", null=True, blank=True)
    role = models.CharField("Роль", max_length=250)
    description = models.TextField("Опис", blank=True)

    family = models.ManyToManyField('self', blank=True, symmetrical=True, verbose_name="Родичі")
    photo = models.ImageField(upload_to='images/characters/', null=True, blank=True)

    anime = models.ForeignKey(
        'anime.Anime',
        on_delete=models.CASCADE,
        related_name='characters',
        verbose_name='Аніме'
    )


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Герой"
        verbose_name_plural = "Герої"