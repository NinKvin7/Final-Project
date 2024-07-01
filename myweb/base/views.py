from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie, User, Genre
from django.db.models import Q

# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    movies = Movie.objects.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(actor__name__icontains=q) | Q(genre__name__icontains=q) )
    movies = list(set(movies))
    # movies = Movie.objects.all()
    heading = " Movies "
    genres = Genre.objects.all()
    context = {"movies": movies, "heading": heading, "genres": genres}
    return render(request, 'base/home.html', context)

def about(request):
    return render(request, 'base/about.html')

def profile(request, pk):
    user = User.objects.get(id=pk)
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    movies = user.movies.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(actor__name__icontains=q) | Q(genre__name__icontains=q))
    movies = list(set(movies))
    # movies=user.movies.all()
    heading = " My movies "
    genres = Genre.objects.all()
    context = {"movies": movies, "heading": heading, "genres": genres}
    return render(request, 'base/profile.html', context)
