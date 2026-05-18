import sys
from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        from django.contrib.auth import get_user_model
        from profiles.models import Profile

        if 'runserver' in sys.argv:
            try:
                User = get_user_model()
                for user in User.objects.all():
                    Profile.objects.get_or_create(user=user)
            except Exception:
                pass