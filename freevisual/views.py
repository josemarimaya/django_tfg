
# Imports de django
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate # Creación de cookies
from django.contrib.auth import get_user_model # Depuración
from django.db.models import Q
# Imports del propio proyecto
from .models import Creator, Image, Provinces, Brand, Work, Tags
from .forms import CreateCreatorForm, LoginForm, UploadImageForm, EditProfileForm, EditImageForm_v2, EditImageForm

from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from django.http import HttpResponseForbidden 


def index(request):
    # Le marcamos que queremos las 9 más recientes, es decir por orden inverso de la lista '-uploaded_at'
    recent_images = Image.objects.order_by('-uploaded_at')[:9]
    return render(request,'index.html', {
        'images': recent_images
    })

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

    query = request.GET.get('query', '')
  
    # Si el usuario está autenticado, puede buscar todas las etiquetas
    if request.user.is_authenticated:
        if query == '':
            images = Image.objects.all()
        else:
            # Usamos Q para usar varios filtros al mismo tiempo
            images = Image.objects.filter(
                Q(title__icontains=query) |  # Filtra por título
                Q(tags__name__icontains=query)  # Filtra por etiquetas
            ).distinct()
    else:
        # Si el usuario no está autenticado, filtrar solo imágenes con etiquetas no pro
        if query == '':
            images = Image.objects.all()  # Filtrar solo imágenes con etiquetas no pro
        else:
            images = Image.objects.filter(
                (Q(title__icontains=query) | Q(tags__name__icontains=query)) &  # Filtra por título o etiquetas
                Q(tags__is_pro=False)  # Solo etiquetas no pro
            ).distinct()
        

    return render(request, 'gallery.html', {
        'images': images,
        'query': query,
    })

def search_result(request):
    query = request.GET.get('query', '')

    selected_brands = request.GET.getlist('brand')  
    selected_provinces = request.GET.getlist('province') 
    selected_works = request.GET.getlist('work')

    brands = Brand.objects.all()
    provinces = Provinces.objects.all()
    works = Work.objects.all()

    if query:
        creators = Creator.objects.filter(
            Q(username__icontains= query) | Q(work__name__icontains=query))
    else:
        creators = Creator.objects.all()

    if selected_brands:
        creators = creators.filter(brand__id__in=selected_brands)

    if selected_provinces:
        creators = creators.filter(provinces__id__in=selected_provinces)

    if selected_works:
        creators = creators.filter(work__id__in=selected_works)
    
    creators = creators.distinct()
    

    return render(request, 'search_results.html', {
        'creators': creators,
        'query': query,
        'brands': brands,
        'provinces': provinces,
        'works': works,
        'selected_brands': selected_brands,
        'selected_provinces': selected_provinces,
        'selected_works': selected_works
    })

def go_profile(request, profile_id):

    creator = get_object_or_404(Creator, id = profile_id)

    images_from_creator = Image.objects.filter(owner = profile_id)

    profile_pic = creator.profile_pic.url if creator.profile_pic else '/media/images/galactus.png'

    provinces =creator.provinces.all()

    brands = creator.brand.all()

    works = creator.work.all()

    return render(request, 'profile_html/profile_search.html',{
        'creator': creator,
        'images': images_from_creator,
        'profile_pic': profile_pic,
        'provinces': provinces,
        'brands': brands,
        'works': works
    })


def profile(request):
    images_from_user = Image.objects.filter(owner = request.user)

    profile_pic = request.user.profile_pic.url if request.user.profile_pic else '/media/images/galactus.png'

    provinces = request.user.provinces.all()

    brands = request.user.brand.all()

    works = request.user.work.all()

    print(provinces)

    print(brands)

    return render(request, 'profile_html/profile.html', {
        'range': range(9),
        'images': images_from_user,
        'profile_pic': profile_pic,
        'provinces': provinces,
        'brands': brands,
        'works': works
    })

def edit_profile(request, profile_id):
    
    profile = get_object_or_404(Creator, id=profile_id)

    if request.user != profile:
        return HttpResponseForbidden("No puedes editar este perfil.")

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirige al perfil una vez guardado
    else:
        form = EditProfileForm(instance=profile)

    
    return render(request, 'profile_html/edit_profile.html', {
        'profile': profile,
        'form': form
    })


def upload(request):

    if request.method == 'GET':
        return render(request, 'upload.html', {
            'form': UploadImageForm()
        })
    
    elif request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            
            # Asignar el propietario de la imagen
            if isinstance(request.user, Creator):
                image.owner = request.user
                image.save()
                # Para relaciones ManyToMany como 'tagged_creators'
                form.save_m2m()  

                if 'edit_button' in request.POST:
                    return redirect(reverse('edit_image', args=[image.id]))
                else:
                    return redirect('main')
            else:
                return HttpResponseForbidden("El usuario autenticado no es un usuario válido.")
            
    return render(request, 'upload.html', {'form': form})


def image_detail(request, image_id):
    
    image = get_object_or_404(Image, pk=image_id)
    creator = image.owner
    tagged_creators = image.tagged_creators.all()
    tags = image.tags.all()
    
    
    return render(request, 'image_html/image_detail.html',{
        'image': image,
        'creator': creator,
        'tagged_creators': tagged_creators,
        'tags': tags
        
    })


def edit_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    if request.user != image.owner:
        return HttpResponseForbidden("No tienes permiso para editar esta imagen.")

    if request.method == 'POST':
        form = EditImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditImageForm(instance=image)
    
    pro_tags = Tags.objects.filter(is_pro = True)
    non_pro_tags = Tags.objects.filter(is_pro = False)
    return render(request, 'image_html/edit_image.html', {
        'form': form, 
        'image': image,
        'valid_tags': {
            'pro': pro_tags,
            'non_pro': non_pro_tags
        }
        })


def delete_image(request, image_id):
    image = get_object_or_404(Image, pk=image_id)

    # Verifica que el usuario autenticado sea el dueño de la imagen
    if request.method == 'POST':
        image.delete()
        return redirect('profile')
    
def delete_image_main(request, image_id):
    image = get_object_or_404(Image, pk=image_id)

    # Verifica que el usuario autenticado sea el dueño de la imagen
    if request.method == 'POST':
        image.delete()
        return redirect('main')
    