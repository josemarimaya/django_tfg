import pytest
from freevisual.models import Creator, Image


@pytest.mark.django_db
def test_image_tagged_creators():
    creator1 = Creator.objects.create(username='creator1', email='creator1@example.com', password='pass')
    creator2 = Creator.objects.create(username='creator2', email='creator2@example.com', password='pass')
    
    image = Image.objects.create(
        owner=creator1,
        image='images/test_image.png',
        title='Tagged Creators Image',
        description='Test image with tagged creators'
    )
    
    # Etiquetamos a los creadores en la imagen
    image.tagged_creators.add(creator1, creator2)
    
    assert image.tagged_creators.count() == 2
    assert creator1 in image.tagged_creators.all()
    assert creator2 in image.tagged_creators.all()
