from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_inicio_sesion():
    # Configuración de opciones para Chrome (Crucial para que corra en GitHub Actions)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # No abre la ventana gráfica (obligatorio para servidores)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Inicializar el navegador Chrome con las opciones configuradas
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        # 1. Abrir la página de login
        driver.get("https://the-internet.herokuapp.com/login")

        # 2. Capturar usuario y contraseña e ingresar datos
        usuario = driver.find_element(By.ID, "username")
        usuario.send_keys("tomsmith")

        password = driver.find_element(By.ID, "password")
        password.send_keys("SuperSecretPassword!")

        # 3. Iniciar sesión (Hacer clic en el botón de submit)
        boton_login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        boton_login.click()

        # 4. Validar mensaje exitoso 
        # Esperamos un máximo de 10 segundos a que el elemento del mensaje esté presente
        mensaje_exito = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "flash"))
        )
        assert "You logged into a secure area!" in mensaje_exito.text

    finally:
        # 5. Cerrar navegador de manera segura al terminar
        driver.quit()