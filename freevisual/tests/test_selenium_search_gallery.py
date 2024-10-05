import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

@pytest.mark.django_db
class TestGallerySearch(StaticLiveServerTestCase):

    def setUp(self):
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(5)  
        self.driver.set_window_size(1920, 1080) 

    def tearDown(self):
        time.sleep(5)
        self.driver.quit()

    def test_gallery_search(self):
        # Navegamos a la página de Gallery desde la barra de navegación
        self.driver.get(self.live_server_url)

        # Acceder a la URL de la galería
        gallery_url = reverse('gallery')
        self.driver.get(f"{self.live_server_url}{gallery_url}")

        # Esperamos hasta que se cargue el campo de búsqueda de la galería
        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "query"))
        )

        # Buscamos un término en la galería
        search_input.send_keys('landscape')
        search_input.send_keys(Keys.RETURN)

        # Esperamos a que la página se actualice o se mantenga en la misma URL con los resultados
        WebDriverWait(self.driver, 10).until(
            EC.url_contains(gallery_url)
        )

        # Verificamos que la página sigue siendo la de galería
        assert "Esta es la galería" in self.driver.page_source  
        # Verificamos que la página muestra resultados relacionados con "landscape"
        assert "landscape" in self.driver.page_source  #
