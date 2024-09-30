import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from freevisual.models import Creator


@pytest.mark.django_db
class TestSearchProfessionals(StaticLiveServerTestCase):

    def setUp(self):
       
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)  # Espera máxima de 10 segundos por cada acción

        # Ajustar el tamaño de la ventana del navegador, porque sino no podrá encontrar el navegador
        self.driver.set_window_size(1920, 1080)  

    def tearDown(self):
        # Espera antes de cerrarse el navegador de prueba
        time.sleep(5)
        
        self.driver.quit()



    def test_search_professionals(self):
        # Abrimos la página de creación de usuario
        self.driver.get(f'{self.live_server_url}{reverse("sign_up")}')

        # Rellenamos el formulario de registro
        name_input = self.driver.find_element(By.NAME, 'name')
        username_input = self.driver.find_element(By.NAME, 'username')
        email_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')
        password2_input = self.driver.find_element(By.NAME, 'password2')

        name_input.send_keys('Test User')
        username_input.send_keys('testuser')
        email_input.send_keys('testuser@example.com')
        password_input.send_keys('Testpassword123')
        password2_input.send_keys('Testpassword123')
        password2_input.send_keys(Keys.RETURN)


        # Verificar que la página ha redirigido después de iniciar sesión
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.current_url == f'{self.live_server_url}{reverse("main")}'
        )

        # Buscar un profesional en la barra de búsqueda
        search_input = self.driver.find_element(By.NAME, "query")
        search_input.send_keys('fotógrafo')
        search_input.send_keys(Keys.RETURN)

        # Verificar que se redirige a la página de resultados de búsqueda
        WebDriverWait(self.driver, 10).until(
            lambda driver: reverse('search') in driver.current_url
        )

        # Confirmar que se muestra el resultado en la página
        assert "Resultados de búsqueda para" in self.driver.page_source
