
from django.shortcuts import render
from .models import Creator
# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request, 'about.html')

def sign_in(request):
    return render(request, 'signin.html')

def sign_up(request):
    return render(request, 'signup.html')

def gallery(request):
    return render(request, 'gallery.html')

def profile(request):
    return render(request, 'profile.html')

def upload(request):
    return render(request, 'upload.html')