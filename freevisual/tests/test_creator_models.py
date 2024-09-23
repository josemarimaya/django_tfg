import pytest
from freevisual.models import Creator  # Asegúrate de que el import esté correcto

@pytest.mark.django_db
def test_create_creator():
    creator = Creator.objects.create_user(
        username="testuser", 
        password="secret", 
        email="testuser@example.com",
        name = "test",
        surname = "user"
    )
    assert creator.username == "testuser"
    assert creator.check_password("secret")

