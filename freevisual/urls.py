from django.urls import path, include
from . import views # Importamos las views directamente desde la app

urlpatterns = [
    path('', views.index, name='main'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('signin/', views.sign_in_2, name='sign_in'),
    path('signup/', views.sign_up, name='sign_up'),
    path('post_content/', views.upload, name='upload'),
    path('profile/', views.profile, name='profile'),
    path('signout/', views.signout, name='sign_out')
]