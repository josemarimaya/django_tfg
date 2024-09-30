import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from freevisual.models import Creator

@pytest.mark.django_db
class TestSignUpAndUploadImage(StaticLiveServerTestCase):
    def setUp(self):
        # Configuración del driver de Selenium
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        # Urls
        self.sign_up_url = self.live_server_url + reverse('sign_up')
        self.upload_url = self.live_server_url + reverse('upload')

        self.driver.set_window_size(1920, 1080)  

    def tearDown(self):
        time.sleep(5)
        self.driver.quit()

    def test_create_user_and_upload_image(self):
       
        self.driver.get(self.sign_up_url)
        
        # Rellenar el formulario de registro
        self.driver.find_element(By.NAME, 'name').send_keys('Test User')
        self.driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.driver.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        self.driver.find_element(By.NAME, 'password').send_keys('password123')
        self.driver.find_element(By.NAME, 'password2').send_keys('password123')
        
        # Hacer submit buscando el botón por su texto
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]").click()

        # Verificar que el usuario ha sido creado y autenticado
        creator = Creator.objects.filter(username='testuser').exists()
        assert creator is True

        # Subida de imagen
        self.driver.get(self.upload_url)

        # Obtener el path de la imagen de prueba
        image_path = os.path.join(os.getcwd(), 'freevisual/tests', 'testing.jpg')

        # Rellenar el formulario de subida de imagen
        self.driver.find_element(By.NAME, 'title').send_keys('Test Image')
        self.driver.find_element(By.NAME, 'description').send_keys('This is a test description.')
        self.driver.find_element(By.NAME, 'image').send_keys(image_path)

        # Hacer submit para subir la imagen
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sube tu imagen')]").click()

        # Verificar si la imagen ha sido subida con éxito (redirige al 'main')
        # Esperamos que la URL sea la de la vista 'main'
        assert self.driver.current_url == f'{self.live_server_url}/'

