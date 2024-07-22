from django.urls import path, include
from . import views # Importamos las views directamente desde la app

urlpatterns = [
    path('', views.index)
    
]