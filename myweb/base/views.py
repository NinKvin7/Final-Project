from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Movie, User, Genre, Director, Actor, Country
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, MovieForm
# from .seeder import seeder_func
from django.contrib import messages

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

@login_required(login_url='login')
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

def adding(request, id):
    user = request.user
    movie = Movie.objects.get(id=id)
    user.movies.add(movie)

    return redirect('profile', user.id)

def delete(request, id):
    obj = Movie.objects.get(id=id)


    if request.method == "POST":
        request.user.movies.remove(obj)
        return redirect('profile', request.user.id)

    return render(request, 'base/delete.html', {'obj': obj})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.id)

    if request.method =='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            pass

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile', request.user.id)
        else:
            pass



    return render(request, 'base/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('profile', user.id)

        else:
            pass
            # messages.error(request, 'Follow The Instructions and create proper user and password...')

    context = {'form': form}
    return render(request, 'base/register.html', context)

def add_movie(request):
    directors = Director.objects.all()
    actors = Actor.objects.all()
    genres = Genre.objects.all()
    countries = Country.objects.all()
    form = MovieForm()

    if request.method == 'POST':
        movie_director = request.POST.get('director')
        movie_actor = request.POST.get('actor')
        movie_genre = request.POST.get('genre')
        movie_country = request.POST.get('country')

        director, created = Director.objects.get_or_create(name=movie_director)
        actor, created = Actor.objects.get_or_create(name=movie_actor)
        genre, created = Genre.objects.get_or_create(name=movie_genre)
        country, created = Country.objects.get_or_create(name=movie_country)

        form = MovieForm(request.POST)

        new_movie = Movie(picture=request.FILES['picture'], name=form.data['name'], director=director,
                        description=form.data['description'], file=request.FILES['file'],
                        year = form.data['year'], rate=form.data['rate'],
                        runtime=form.data['runtime'], trailer= form.data['trailer'])


        new_movie.save()
        new_movie.actor.add(actor)
        new_movie.genre.add(genre)
        new_movie.country.add(country)

        return redirect('home')



    context = {'form': form, 'directors': directors, 'actors':actors, 'genres': genres, 'countries': countries}
    return render(request, 'base/add_movie.html', context)