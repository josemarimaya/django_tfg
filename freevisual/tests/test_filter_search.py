
import pytest
from freevisual.models import Creator, Brand, Provinces

@pytest.mark.django_db
def test_search_creators_by_brand_and_province():
    creator1 = Creator.objects.create(username='creator1', email='creator1@example.com', password='pass')
    #creator2 = Creator.objects.create(username='creator2', email='creator2@example.com', password='pass')

    brand = Brand.objects.create(name='Canon')
    province = Provinces.objects.create(name='Madrid')

    creator1.brand.add(brand)
    creator1.provinces.add(province)
    
    # Simulamos una búsqueda por marca y provincia
    results = Creator.objects.filter(brand=brand, provinces=province)

    assert len(results) == 1
    assert results[0] == creator1
