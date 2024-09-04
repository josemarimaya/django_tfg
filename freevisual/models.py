# Imports de django
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Imports para poder usar el auth
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Field(models.Model):
    name = models.CharField(max_length=200)

class Speciality(models.Model):
    name = models.CharField(max_length=200)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)


class Tools(models.Model):
    name = models.CharField(max_length=200)


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
    username = models.CharField(max_length=200, default='')
    email = models.EmailField(unique=True) # Los emails debes de ser únicos
    password = models.CharField(max_length=200)
    tools = models.ManyToManyField('Tools', verbose_name="Lista de herramientas del creador")
    specialities = models.ManyToManyField('Speciality', verbose_name="Lista de especialidades del creador")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = CreatorManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='creator_set',  # Se cambia el nombre de la relación para evitar conflicto
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='creator_permission_set',  # Se cambia el nombre de la relación para evitar conflicto
        blank=True
    )

    def __str__(self):
        return self.email
    
"""class Creator(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    password = models.CharField(max_length=200, default="")
    email =  models.CharField(max_length=200)
    tools =  models.ManyToManyField(Tools, verbose_name="Lista de herramientas del creador")
    specialities =  models.ManyToManyField(Speciality, verbose_name="Lista de especialidades del creador")
"""



class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='images/', default='images/galactus.png')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now )

    def __str__(self):
        return self.title
    