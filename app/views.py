from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

# from .forms import 
# from .models import 


def home(request):
    c = {}
    return render(request, 'app/home.html', c)