# tests/test_selenium_edit_profile.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.mark.django_db
class TestEditProfile(StaticLiveServerTestCase):
    def setUp(self):
        # Configurar el driver de Selenium (Chrome)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)  # Espera máxima de 10 segundos por cada acción

    def tearDown(self):
        # Cerrar el navegador después de cada prueba
        self.driver.quit()

    def test_create_user_and_edit_profile(self):
        # Abrir la página de registro
        self.driver.get(f'{self.live_server_url}{reverse("sign_up")}')

        # Rellenar el formulario de registro
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

        # Verificar si el usuario fue redirigido a la página principal
        assert self.driver.current_url == f'{self.live_server_url}{reverse("main")}'

        # Iniciar sesión (en caso de no estar logueado automáticamente)
        self.driver.get(f'{self.live_server_url}{reverse("sign_in")}')
        username_login_input = self.driver.find_element(By.NAME, 'username')
        password_login_input = self.driver.find_element(By.NAME, 'password')

        username_login_input.send_keys('testuser')
        password_login_input.send_keys('Testpassword123')
        password_login_input.send_keys(Keys.RETURN)

        # Ir a la página de editar perfil
        self.driver.get(f'{self.live_server_url}{reverse("edit_profile", kwargs={"profile_id": 1})}')
        
        # Editar campos del perfil (en este caso, la descripción)
        description_input = self.driver.find_element(By.NAME, 'description')
        description_input.clear()
        description_input.send_keys('This is the updated description.')

        # Enviar el formulario
        description_input.send_keys(Keys.RETURN)

        # Verificar si la descripción fue actualizada correctamente
        assert 'This is the updated description.' in self.driver.page_source
