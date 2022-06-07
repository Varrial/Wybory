from django.http import HttpResponse
from django.shortcuts import render
from .models import Wybory

def home(request):
    wybory = Wybory.objects.all()
    context = {'wybory': wybory}
    return render(request, 'home/home.html', context)

def wybory(request, pk):
    return render(request, 'home/wybory.html')