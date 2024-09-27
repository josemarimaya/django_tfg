import pytest
from django.utils import timezone
from freevisual.models import Image, Creator, Tags

@pytest.mark.django_db
def test_create_image():
   # Creamos el Creator igual que en el test para creator
    creator = Creator.objects.create(
        username='creator_test',
        email='test@example.com',
        password='testpassword123'
    )
    
    # Creamos una etiqueta para asociarla con la imagen
    tag = Tags.objects.create(name='nature', is_pro=False)
    
    # Creamos una imagen de prueba
    image = Image.objects.create(
        owner=creator,
        image='images/test_image.png',
        title='Test Image',
        description='This is a test image description',
        uploaded_at=timezone.now()
    )
    
    # Asociamos la etiqueta a la imagen
    image.tags.add(tag)

    # Verificamos que la imagen fue creada correctamente
    assert image.owner == creator
    assert image.title == 'Test Image'
    assert image.description == 'This is a test image description'
    assert image.tags.count() == 1
    assert image.tags.first().name == 'nature'
