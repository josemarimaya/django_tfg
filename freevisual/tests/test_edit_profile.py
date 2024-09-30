import pytest
from freevisual.models import Creator, Provinces, Brand, Work
from freevisual.forms import EditProfileForm

@pytest.mark.django_db
def test_edit_profile_form():
    # Creación del creador
    creator = Creator.objects.create(username='creator_test', email='test@example.com', password='testpassword123')

    # Creación de instancias para Provinces, Brand y Work
    province1 = Provinces.objects.create(name="Madrid")
    province2 = Provinces.objects.create(name="Barcelona")
    brand1 = Brand.objects.create(name="Canon")
    brand2 = Brand.objects.create(name="Nikon")
    work1 = Work.objects.create(name="Fotógrafo")
    work2 = Work.objects.create(name="Editor de Video")

    # Datos del formulario de edición
    form_data = {
        'description': 'Actualización de descripción',
        'provinces': [province1.id, province2.id],
        'brand': [brand1.id, brand2.id],
        'work': [work1.id, work2.id],
    }

    # Creamos el formulario con datos y el creador original
    form = EditProfileForm(data=form_data, instance=creator)

    # Verificamos que el formulario es válido
    assert form.is_valid()

    # Guardamos los cambios
    updated_creator = form.save()

    # Verificamos que los datos del creador han sido actualizados correctamente
    assert updated_creator.description == 'Actualización de descripción'
    assert list(updated_creator.provinces.all()) == [province1, province2]
    assert list(updated_creator.brand.all()) == [brand1, brand2]
    assert list(updated_creator.work.all()) == [work1, work2]

