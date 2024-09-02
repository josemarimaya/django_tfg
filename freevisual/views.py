
# Imports de django
from django.shortcuts import render, redirect

# Imports del propio proyecto
from .models import Creator
from .forms import CreateCreatorForm

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request, 'about.html')

def sign_in(request):
    return render(request, 'signin.html')

def sign_up(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CreateCreatorForm
        })
    else:
        
        if request.POST['password'] == request.POST['password2']:
            
            Creator.objects.create(name=request.POST['name'], 
                password=request.POST['password'], email= request.POST['email'])
            return redirect('main')
        else:

            return render(request, 'signup.html', {
                'form': CreateCreatorForm,
                'error': 'Las contraseñas no coinciden'
            })

    

def gallery(request):
    return render(request, 'gallery.html')

def profile(request):
    return render(request, 'profile.html')

def upload(request):
    return render(request, 'upload.html')