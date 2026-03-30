from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Ця функція спрацьовує одразу ПІСЛЯ створення нового User.
    'created' буде True тільки при першому створенні об'єкта.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    При будь-якому оновленні даних User (наприклад, зміна пароля),
    ми також перезберігаємо пов'язаний Profile.
    """
    instance.profile.save()