from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User

# from .models import


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
        new_user = User.objects.create_user(
            username=request.POST['username'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        new_user.save()

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            c['error'] = 'Sign up failed. Please try again.'

    return render(request, 'app/signup.html', c)


@login_required
def albums(request):
    c = {}
    return render(request, 'app/albums.html', c)

@login_required
def favorites(request):
    c = {}
    return render(request, 'app/favorites.html', c)
