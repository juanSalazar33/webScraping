# Web Scraping de LinkedIn

Este proyecto permite extraer información básica de perfiles de LinkedIn de manera automatizada.

## Características

- Inicio de sesión automático en LinkedIn
- Extracción de nombre y título del perfil
- Almacenamiento de la información en un archivo de texto con fecha y hora
- Opción para borrar registros anteriores

## Requisitos

- Python 3.6+
- Selenium
- Chrome WebDriver

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Descargar [Chrome WebDriver](https://sites.google.com/chromium.org/driver/) compatible con tu versión de Chrome

## Uso

1. Editar el archivo `main.py` para agregar tus credenciales de LinkedIn
2. Ejecutar el script: `python main.py`
3. Para borrar registros anteriores, usar la función `borrar_registros()`

## Notas importantes

- Este script es solo para fines educativos
- El uso excesivo de web scraping puede violar los términos de servicio de LinkedIn
- Se recomienda agregar pausas entre solicitudes para evitar ser bloqueado