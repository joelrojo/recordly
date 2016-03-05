from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.contrib.auth.models import User

from datetime import datetime
import json
import uuid

from .models import Song, Artist, Album


def create_unique_key(unique_ids):
    hash_string = "-".join(unique_ids)
    hash_string = '%s!%s' % (hash_string, settings.KEY_SALT)
    u = uuid.uuid3(uuid.NAMESPACE_URL, hash_string.encode('utf8'))
    return u.hex


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


@require_POST
@login_required
def favorite_item(request):
    c = {}
    data = request.POST

    album = get_object_or_404(Album, key=data.get('key'))
    if data.get("favorited") == 'true':
        album.favorited = False
        c['msg'] = 'removed'
    else:
        album.favorited = True
        c['msg'] = 'added'
    album.save()
    return HttpResponse(json.dumps(c), content_type='application/json')


@require_POST
@login_required
def add_album(request):
    c = {}
    data = request.POST

    print data.get('title')
    print data.get('artist')
    print data.get('song')

    # check for duplicates
    if Album.objects.filter(title=data.get('title'), user=request.user).exists():
        print "album exists"
        c['error_msg'] = 'Album exists. Please try another title.'
        return HttpResponse(json.dumps(c), content_type='application/json')

    if Artist.objects.filter(name=data.get('artist')).exists():
        c['error_msg'] = 'Artist exists. Please try again.'
        return HttpResponse(json.dumps(c), content_type='application/json')

    if Song.objects.filter(title=data.get('song')).exists():
        c['error_msg'] = 'Song exists. Please try again.'
        return HttpResponse(json.dumps(c), content_type='application/json')

    # generate unique key and create artist
    _u = [str(request.user.username), str(datetime.now())]
    unique_key = create_unique_key(_u)[:8]

    while Artist.objects.filter(key=unique_key).exists():
        _u = [str(request.user.username), str(datetime.now())]
        unique_key = create_unique_key(_u)[:8]

    artist_obj = Artist(key=unique_key, name=data.get('artist'))
    artist_obj.save()

    # generate unique key and create song
    _u = [str(request.user.username), str(datetime.now())]
    unique_key = create_unique_key(_u)[:8]

    while Song.objects.filter(key=unique_key).exists():
        _u = [str(request.user.username), str(datetime.now())]
        unique_key = create_unique_key(_u)[:8]

    song_obj = Song(key=unique_key, title=data.get('song'))
    song_obj.save()

    # generate unique key for album
    _u = [str(request.user.username), str(datetime.now())]
    unique_key = create_unique_key(_u)[:8]

    while Album.objects.filter(key=unique_key).exists():
        _u = [str(request.user.username), str(datetime.now())]
        unique_key = create_unique_key(_u)[:8]

    album = Album(
        key=unique_key,
        title=data.get('title'),
        artist=artist_obj,
        user=request.user
    )
    album.save()
    album.songs.add(song_obj)
    album.save()

    c['success'] = True
    return HttpResponse(json.dumps(c), content_type='application/json')
