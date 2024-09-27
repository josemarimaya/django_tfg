import pytest
from freevisual.models import Image, Creator

from django.core.exceptions import ValidationError

# Este test nos sirve para comprobar los fallos al no rellenar los campos obligatorios
@pytest.mark.django_db
def test_image_creation_without_required_fields():
    creator = Creator.objects.create(username='creator_test', email='test@example.com', password='testpassword123')
    
    # Intentamos crear una imagen sin campos obligatorios (sin image y title)
    with pytest.raises(ValidationError):
        image = Image(
            owner=creator,
            description='Missing required fields'
        )
        image.full_clean()  # Esto valida el modelo, lanzando el error de validación
