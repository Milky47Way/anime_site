from django.contrib import admin
from .models import Anime, Author, DubStudio

admin.site.register(Anime)
admin.site.register(Author)
admin.site.register(DubStudio)