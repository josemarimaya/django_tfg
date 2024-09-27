import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.mark.django_db
class TestSignUp(StaticLiveServerTestCase):
    def setUp(self):
        # Configurar el driver de Selenium (Chrome)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)  # Espera máxima de 10 segundos por cada acción

    def tearDown(self):
        # Cerrar el navegador después de cada prueba
        self.driver.quit()

    def test_sign_up(self):
        # Abrir la página de registro
        self.driver.get(f'{self.live_server_url}{reverse("sign_up")}')

        # Rellenar el formulario de registro usando los 'name' de cada campo
        name_input = self.driver.find_element(By.NAME, 'name')
        username_input = self.driver.find_element(By.NAME, 'username')
        email_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')
        password2_input = self.driver.find_element(By.NAME, 'password2')

        # Simulamos el envío del formulario con los datos de prueba
        name_input.send_keys('Test User')
        username_input.send_keys('testuser')
        email_input.send_keys('testuser@example.com')
        password_input.send_keys('Testpassword123')
        password2_input.send_keys('Testpassword123')

        # Enviar el formulario
        password2_input.send_keys(Keys.RETURN)

        # Verificar si el usuario fue redirigido a la página principal
        assert self.driver.current_url == f'{self.live_server_url}{reverse("main")}'