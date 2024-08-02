from django.urls import path, include
from . import views # Importamos las views directamente desde la app

urlpatterns = [
    path('', views.index, name='main'),
    path('about/', views.about, name='about'),
    path('signin/', views.sign_in, name='sign_in'),
    path('signup/', views.sign_up, name='sign_up')
]