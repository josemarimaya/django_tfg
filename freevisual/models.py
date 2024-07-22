from django.db import models

# Create your models here.

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
    email =  models.CharField(max_length=200)
    tools =  models.ManyToManyField(Tools, verbose_name="Lista de herramientas del creador")
    specialities =  models.ManyToManyField(Speciality, verbose_name="Lista de especialidades del creador")