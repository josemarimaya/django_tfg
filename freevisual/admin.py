from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Creator)
admin.site.register(models.Speciality)
admin.site.register(models.Field)
admin.site.register(models.Tools)
