from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User

from .models import Song, Artist, Album


def home(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)

    c = {}
    return render(request, 'home.html', c)


def login_user(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)

    c = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            c['error'] = 'Log in failed. Please try again.'

    return render(request, 'app/login.html', c)


def logout_user(request):
    logout(request)
    return redirect('/')


def signup_user(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)

    c = {}
    if request.method == 'POST':
        try:
            new_user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password']
            )
            new_user.save()
            print "NEW USER"
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )
            print "USER AUTH"
            if user is not None:
                login(request, user)
                print "USER LOGIN"
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                c['error'] = 'Login failed. Please try again.'
        except:
            c['error'] = 'That username already exists.'

    return render(request, 'app/signup.html', c)


@login_required
def albums(request):
    c = {}
    c['albums'] = Album.objects.filter(user=request.user)
    return render(request, 'app/albums.html', c)


@login_required
def favorites(request):
    c = {}
    c['albums'] = Album.objects.filter(user=request.user, favorited=True)
    c['songs'] = Song.objects.filter(favorited=True)
    c['artists'] = Artist.objects.filter(favorited=True)
    return render(request, 'app/favorites.html', c)


@login_required
def album_page(request, key):
    c = {}
    album = get_object_or_404(Album, key=key)
    c['album'] = album
    return render(request, 'app/single/album.html', c)


@login_required
def song_page(request, key):
    c = {}
    song = get_object_or_404(Song, key=key)
    c['song'] = song
    return render(request, 'app/single/song.html', c)


@login_required
def artist_page(request, key):
    c = {}
    artist = get_object_or_404(Artist, key=key)
    c['artist'] = artist
    return render(request, 'app/single/artist.html', c)
