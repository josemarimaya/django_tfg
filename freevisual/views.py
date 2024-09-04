
# Imports de django
from django.shortcuts import render, redirect

# Imports del propio proyecto
from .models import Creator
from .forms import CreateCreatorForm, LoginForm
from django.contrib.auth import login, logout, authenticate # Creación de cookies
from django.contrib.auth import get_user_model # Depuración
from django.contrib.auth.hashers import check_password

def index(request):
    return render(request,'index.html')

def about(request):
    users = Creator.objects.all()
    print(users)
    return render(request, 'about.html')

def sign_in(request):

    if request.method == 'POST':
        # Depuración de código
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=request.POST['username'])
            print(f"User found: {user}" + "{user.password}")
        except UserModel.DoesNotExist:
            print("User not found.")
            user = None

        user_authenticate = authenticate(request, username=request.POST['username'],
            password=request.POST['password'])
        print(request.POST['username'])
        print(request.POST['password'])
        print(user_authenticate)
        
        if user_authenticate is None:
            return render(request, 'signin.html', {
                'error': 'El usuario o la contraseña es incorrecta',
                'form': LoginForm
            })
        else:
            login(request, user_authenticate)
            return redirect('main')
    
    return render(request, 'signin.html', {
        'form': LoginForm
    })

def sign_in_2(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        UserModel = get_user_model()
        print(UserModel)
        try:
            # Buscar el usuario por su nombre de usuario
            user = UserModel.objects.get(username=username)
            print(user)
        except UserModel.DoesNotExist:
            # Si el usuario no existe, mostrar error
            return render(request, 'signin.html', {
                'error': 'El usuario o la contraseña es incorrecta',
                'form': LoginForm()
            })

        # Verificar si la contraseña proporcionada es correcta
        if user.password == password: # Tenemos un problema con el cifrado de las contraseñas pero con esta comprobación tenemos suficiente
            # La contraseña es correcta, iniciar sesión
            login(request, user)
            return redirect('main')
        else:
            # Contraseña incorrecta
            return render(request, 'signin.html', {
                'error': 'El usuario o la contraseña es incorrecta',
                'form': LoginForm()
            })

    return render(request, 'signin.html', {
        'form': LoginForm()
    })

def sign_up(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CreateCreatorForm
        })
    else:
        
        if request.POST['password'] == request.POST['password2']:
            
            creator = Creator.objects.create(name=request.POST['name'], username= request.POST['username'],
                password=request.POST['password'], email= request.POST['email'])
            creator.save()
            login(request,creator)
            return redirect('main')
        else:

            return render(request, 'signup.html', {
                'form': CreateCreatorForm,
                'error': 'Las contraseñas no coinciden'
            })

    
def signout(request):
    logout(request)
    return redirect('main')

def gallery(request):
    return render(request, 'gallery.html')

def profile(request):
    return render(request, 'profile.html')

def upload(request):
    return render(request, 'upload.html')