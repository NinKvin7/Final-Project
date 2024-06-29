from django.db import models

# Create your models here.

class Movie(models.Model):
    picture = models.CharField(max_length=300)
    name = models.CharField(max_length=50)
    rate = models.FloatField(max_length=5)
    year = models.IntegerField(max_length=5)
    genre = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.name} _ {self.year}"


