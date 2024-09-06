from django.urls import path, include
from . import views # Importamos las views directamente desde la app

# Imports de .settings para el tratamiento de archivos
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='main'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('signin/', views.sign_in_2, name='sign_in'),
    path('signup/', views.sign_up, name='sign_up'),
    path('post_content/', views.upload, name='upload'),
    path('profile/', views.profile, name='profile'),
    path('signout/', views.signout, name='sign_out'),
    path('image/<int:image_id>', views.image_detail, name='image_detail'),
    path('edit_image/<int:image_id>/', views.edit_image, name='edit_image'),
    path('image/delete/<int:image_id>/', views.delete_image, name='delete_image'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)