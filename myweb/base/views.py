from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie, User

# Create your views here.


def home(request):
    movies = Movie.objects.all()
    context = {"movies": movies}
    return render(request, 'base/home.html', context)

def about(request):
    return render(request, 'base/about.html')

def profile(request, pk):
    user = User.objects.get(id=pk)
    movies=user.movies.all()
    context = {"movies": movies}
    return render(request, 'base/profile.html', context)
