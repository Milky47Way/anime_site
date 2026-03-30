from django.test import TestCase
from .models import Anime

class AnimeModelTest(TestCase):
    def setUp(self):
        Anime.objects.create(title="Чорна конюшина ", author="Юкі Табата")

        def test_string_representation(self):
            anime = Anime.objects.get(id=1)
            self.assertEqual(str(anime), "Чорна конюшина")
# Create your tests here.
#python manage.py test
