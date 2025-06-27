# Aplicación Web para Envío de Correos con Archivos Adjuntos

Esta es una sencilla aplicación web construida con Flask en Python que permite a los usuarios subir un archivo y enviarlo como adjunto a una dirección de correo electrónico específica a través de Gmail.

## Características

* Interfaz de usuario simple y responsiva (gracias a Tailwind CSS).
* Selección de archivos y previsualización del nombre del archivo.
* Envío de correos electrónicos con archivos adjuntos.
* Manejo de mensajes de éxito/error en el frontend.

## Requisitos

Antes de ejecutar la aplicación, asegúrate de tener instalado Python 3 y `pip` (el gestor de paquetes de Python).

## Configuración

### 1. Obtener una Contraseña de Aplicación de Google

Para que la aplicación pueda enviar correos a través de tu cuenta de Gmail, necesitas generar una "Contraseña de aplicación" en tu configuración de Google. **No uses tu contraseña principal de Gmail.**

Sigue estos pasos:

1.  **Habilita la Verificación en dos pasos (si no lo has hecho ya):**
    * Ve a tu [Cuenta de Google](https://myaccount.google.com/).
    * En el panel de navegación izquierdo, haz clic en **Seguridad**.
    * En "Cómo inicias sesión en Google", haz clic en **Verificación en dos pasos**.
    * Sigue las instrucciones en pantalla para configurarla. Es un requisito para poder generar contraseñas de aplicación.

2.  **Genera la Contraseña de aplicación:**
    * Una vez que la Verificación en dos pasos esté activada, regresa a la sección **Seguridad** de tu Cuenta de Google.
    * En "Cómo inicias sesión en Google", haz clic en **Contraseñas de aplicaciones**.
    * Es posible que se te pida que inicies sesión de nuevo.
    * En la página "Contraseñas de aplicaciones":
        * En el menú desplegable "Seleccionar aplicación", elige **Correo**.
        * En el menú desplegable "Seleccionar dispositivo", elige **Otro (nombre personalizado)**.
        * Introduce un nombre para recordar dónde usas esta contraseña (por ejemplo, "App Flask Enviar Correo") y haz clic en **Generar**.
    * Google te mostrará una contraseña de 16 caracteres. **Cópiala inmediatamente**, ya que no la volverás a ver. Esta es la `CONTRASEÑA_APP_GMAIL` que usarás en tu código.

### 2. Instalar Módulos de Python

Necesitas instalar Flask para ejecutar el servidor web. Abre tu terminal o línea de comandos y ejecuta:

```bash
pip install Flask
```
**Activarservidor**
```bash
git clone https://github.com/jaam-web/Web_envio_de_archivos
cd Web_envio_de_archivos
```
#edita el archivo app.py y coloca el correo que usaras y la contraseña de aplicacioned 
***NO recomiendo usar tu correo personal***

``` bash
python app.py
```
