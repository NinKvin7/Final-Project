from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=70)
    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=70)
    birth = models.DateField(null=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.name}"




class Movie(models.Model):
    picture = models.CharField(max_length=1000)
    name = models.CharField(max_length=70)
    rate = models.FloatField()
    year = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True, blank=True)
    actor = models.ManyToManyField(Actor)
    country = models.ManyToManyField(Country)
    runtime = models.IntegerField()
    genre = models.ManyToManyField(Genre)
    description = models.CharField(max_length=1200)
    trailer = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.name} ({self.year})"



class User(AbstractUser):
    movies = models.ManyToManyField(Movie, related_name='users', blank=True)