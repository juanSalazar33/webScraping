import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

def iniciar_sesion_linkedin(email, password):
    """
    Función para iniciar sesión en LinkedIn
    """
    try:
        # Configurar opciones de Chrome
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--start-maximized")
        
        # Iniciar el navegador
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navegar a la página de inicio de sesión de LinkedIn
        driver.get("https://www.linkedin.com/login")
        
        # Esperar a que cargue la página
        time.sleep(2)
        
        # Ingresar credenciales
        email_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        
        email_input.send_keys(email)
        password_input.send_keys(password)
        
        # Desmarcar la casilla "Keep me logged in" si está marcada
        try:
            # Usar el ID correcto del checkbox según el HTML proporcionado
            remember_checkbox = driver.find_element(By.ID, "rememberMeOptIn-checkbox")
            if remember_checkbox.is_selected():
                remember_checkbox.click()
                print("Casilla 'Keep me logged in' desmarcada")
        except Exception as e:
            print(f"No se pudo encontrar o desmarcar la casilla 'Keep me logged in': {e}")
        
        # Hacer clic en el botón de inicio de sesión
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Esperar a que se complete el inicio de sesión
        time.sleep(5)
        
        # Verificar si el inicio de sesión fue exitoso
        if "feed" in driver.current_url or "checkpoint" in driver.current_url or "dashboard" in driver.current_url:
            print("Inicio de sesión exitoso")
            return driver
        else:
            print("No se pudo iniciar sesión. URL actual:", driver.current_url)
            # Guardar captura de pantalla para depuración
            driver.save_screenshot("error_login.png")
            driver.quit()
            return None
    
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        try:
            driver.quit()
        except:
            pass
        return None

def extraer_info_perfil(driver, url_perfil):
    """
    Función simplificada para extraer solo nombre y título de un perfil de LinkedIn
    y guardar la información en un archivo de texto con fecha
    """
    try:
        print(f"Navegando a {url_perfil}")
        driver.get(url_perfil)
        time.sleep(5)  # Esperar a que cargue la página
        
        # Guardar el HTML para depuración en caso de error
        with open("perfil_linkedin.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        # Intentar diferentes selectores para el nombre
        nombre = None
        selectores_nombre = [
            "//h1[contains(@class, 'text-heading-xlarge')]",
            "//main//h1",
            "//div[contains(@class, 'pv-text-details__left-panel')]//h1"
        ]
        
        for selector in selectores_nombre:
            try:
                nombre_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                nombre = nombre_element.text
                print(f"Nombre encontrado: {nombre}")
                break
            except:
                continue
        
        if not nombre:
            print("No se pudo encontrar el nombre del perfil")
        
        # Intentar diferentes selectores para el título
        titulo = None
        selectores_titulo = [
            "//div[contains(@class, 'pv-text-details__left-panel')]//div[contains(@class, 'text-body-medium')]",
            "//div[contains(@class, 'mt2')]//span[contains(@class, 'text-body-medium')]",
            "//div[contains(@class, 'display-flex')]//span[contains(@class, 'text-body-medium')]"
        ]
        
        for selector in selectores_titulo:
            try:
                titulo_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                titulo = titulo_element.text
                print(f"Título encontrado: {titulo}")
                break
            except:
                continue
        
        if not titulo:
            print("No se pudo encontrar el título del perfil")
        
        # Crear un diccionario con la información extraída
        info_perfil = {
            "nombre": nombre,
            "titulo": titulo
        }
        
        # Guardar la información en un archivo de texto con fecha
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("registros_linkedin.txt", "a", encoding="utf-8") as f:
            f.write(f"=== Registro: {fecha_actual} ===\n")
            f.write(f"URL: {url_perfil}\n")
            f.write(f"Nombre: {nombre}\n")
            f.write(f"Título: {titulo}\n")
            f.write("="*50 + "\n\n")
        
        print(f"Información guardada en registros_linkedin.txt")
        
        return info_perfil
    
    except Exception as e:
        print(f"Error al extraer información del perfil: {e}")
        # Guardar el HTML para depuración
        with open("error_perfil_linkedin.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        return None

# Función para borrar el contenido del archivo de registros
def borrar_registros():
    """
    Función para borrar el contenido del archivo de registros
    """
    try:
        with open("registros_linkedin.txt", "w", encoding="utf-8") as f:
            f.write("")
        print("Archivo de registros borrado correctamente")
    except Exception as e:
        print(f"Error al borrar el archivo de registros: {e}")

def main():
    """
    Función principal para ejecutar el script
    """
    # Credenciales de LinkedIn (reemplaza con tus credenciales)
    email = ""
    password = ""
    
    # URL del perfil a extraer
    url_perfil = "https://www.linkedin.com/in/juanjsalazarmeneses/"
    
    # Borrar registros anteriores (descomenta esta línea si quieres borrar los registros)
    # borrar_registros()
    
    # Iniciar sesión en LinkedIn
    driver = iniciar_sesion_linkedin(email, password)
    
    if driver:
        try:
            # Extraer información del perfil
            info_perfil = extraer_info_perfil(driver, url_perfil)
            
            if info_perfil:
                print("Información extraída con éxito:")
                for clave, valor in info_perfil.items():
                    print(f"{clave}: {valor}")
            else:
                print("No se pudo extraer la información del perfil")
        
        finally:
            # Cerrar el navegador
            driver.quit()
    else:
        print("No se pudo iniciar sesión en LinkedIn")

# Si este script se ejecuta directamente
if __name__ == "__main__":
    main()
