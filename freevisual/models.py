# Imports de django
from django.db import models
from django.db import models
#from django.contrib.auth.models import User
from django.utils import timezone
# Imports para poder usar el auth
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Field(models.Model):
    name = models.CharField(max_length=200)

class Speciality(models.Model):
    name = models.CharField(max_length=200)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

class Work(models.Model):
    name = models.CharField(max_length=200, verbose_name='Tiene experiencia en')

    def __str__(self):
        return self.name

class Provinces(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Tools(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='marca de herramientas', default=1)
    model_tool = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name

# Clase con BaseManager para poder usar el auth con Creator
class CreatorManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, password, **extra_fields)


class Creator(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True, default='') # Deberíamos añadirle unique=True pero ya tenemos a dos usuarios con el mismo username
    email = models.EmailField(max_length=100) # Los emails debes de ser únicos
    password = models.CharField(max_length=200)
    tools = models.ManyToManyField('Tools', verbose_name="Lista de herramientas del creador")
    specialities = models.ManyToManyField('Speciality', verbose_name="Lista de especialidades del creador")
    provinces = models.ManyToManyField('Provinces', verbose_name="Provincias donde trabaja el creador")
    brand = models.ManyToManyField('Brand', verbose_name='Marcas de herramientas con las que ha trabajado')
    work = models.ManyToManyField('Work', verbose_name='Trabajos que ha realizado')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_pic = models.ImageField(blank=True, null= True, upload_to='images/', default='images/camera.jfif')
    description = models.CharField(blank=True, max_length=1000)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = CreatorManager()

    def __str__(self):
        return self.username



class Tags(models.Model):
    name = models.CharField(max_length=200)
    is_pro = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
class Image(models.Model):
    # Añadimos un related_name para que al usar de FK Creator no genere conflicto con tagged_creators
    owner = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='owner')
    #image = models.ImageField(upload_to='images/', default='images/galactus.png', null=False, blank=False)
    image = models.ImageField(upload_to='images/', null=False, blank=False)
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField('Tags', verbose_name='Etiquetas de la imgen')
    tagged_creators = models.ManyToManyField('Creator', verbose_name='Creadores etiquetados', blank=True, related_name='tagged_creators')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    