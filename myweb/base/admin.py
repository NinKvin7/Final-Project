from django.contrib import admin
from .models import Movie, Director, Actor, Country, Genre, User

# Register your models here.

admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(User)