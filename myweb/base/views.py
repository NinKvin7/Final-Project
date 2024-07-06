from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Movie, User, Genre
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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