# Imports de django
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Field(models.Model):
    name = models.CharField(max_length=200)

class Speciality(models.Model):
    name = models.CharField(max_length=200)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)


class Tools(models.Model):
    name = models.CharField(max_length=200)

class Creator(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    password = models.CharField(max_length=200, default="")
    email =  models.CharField(max_length=200)
    tools =  models.ManyToManyField(Tools, verbose_name="Lista de herramientas del creador")
    specialities =  models.ManyToManyField(Speciality, verbose_name="Lista de especialidades del creador")


class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='images/', default='images/galactus.png')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now )

    def __str__(self):
        return self.title
    