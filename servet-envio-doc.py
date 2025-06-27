from flask import Flask, request, render_template_string, jsonify
import smtplib # Módulo para enviar correos usando el protocolo SMTP
from email.mime.text import MIMEText # Para crear la parte de texto plano del correo
from email.mime.multipart import MIMEMultipart # Para crear correos con múltiples partes
# Importamos MIMEBase para adjuntar cualquier tipo de archivo, y encoders para su codificación
from email.mime.base import MIMEBase
from email import encoders
import base64 # Para codificar/decodificar datos en base64
import os # Para operaciones del sistema de archivos (no se usa directamente para guardar archivos aquí)

app = Flask(__name__)

# --- Configuración de tu cuenta Gmail ---
# ¡IMPORTANTE!: Reemplaza estos valores con los tuyos.
# Necesitas una "contraseña de aplicación" de Google aquí, no tu contraseña principal.
USUARIO_GMAIL = "jaamelectronica@gmail.com"  # Tu dirección de correo electrónico de Gmail
CONTRASEÑA_APP_GMAIL = "hhxwwcqgovjasyzg" # La contraseña de aplicación generada por Google

# --- Configuración del servidor SMTP de Gmail ---
SERVIDOR_SMTP = "smtp.gmail.com"
PUERTO_SMTP = 587  # Puerto estándar para SMTP con TLS

def enviar_correo_con_adjunto(destinatario, asunto, cuerpo_mensaje, archivo_data_base64=None, nombre_archivo=None):
    """
    Envía un correo electrónico con un archivo adjunto de cualquier tipo.

    Args:
        destinatario (str): La dirección de correo electrónico del destinatario.
        asunto (str): El asunto del correo electrónico.
        cuerpo_mensaje (str): El contenido del mensaje en texto plano.
        archivo_data_base64 (str, optional): Datos del archivo en formato base64 (incluye prefijo MIME).
                                            Si es None, no se adjunta archivo.
        nombre_archivo (str, optional): El nombre original del archivo a adjuntar.
    """
    try:
        # Crea un objeto MIMEMultipart para el correo.
        mensaje = MIMEMultipart()
        mensaje['From'] = USUARIO_GMAIL
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        # Adjunta el cuerpo del mensaje como texto plano
        mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

        if archivo_data_base64 and nombre_archivo:
            # Los datos base64 del frontend vienen con un prefijo (ej. "data:image/png;base64,...")
            # Separamos el prefijo para obtener el tipo MIME y los datos puros en base64.
            if "," in archivo_data_base64:
                header, base64_string = archivo_data_base64.split(",", 1)
                # Extraer el tipo MIME (ej. 'image/png', 'application/pdf')
                mime_type = header.split(":")[1].split(";")[0]
            else:
                # Si no hay prefijo, asumimos un tipo genérico y los datos son la cadena base64 pura
                mime_type = "application/octet-stream" # Tipo MIME genérico para datos binarios
                base64_string = archivo_data_base64

            # Decodificar los datos base64 a bytes
            archivo_bytes = base64.b64decode(base64_string)

            # Dividir el tipo MIME en tipo principal y subtipo (ej. 'image' y 'png')
            maintype, subtype = mime_type.split('/', 1)

            # Crear un objeto MIMEBase para el adjunto (compatible con cualquier tipo de archivo)
            adjunto = MIMEBase(maintype, subtype)
            adjunto.set_payload(archivo_bytes)
            encoders.encode_base64(adjunto) # Codifica el payload para el transporte por correo

            # Añade una cabecera para indicar que es un adjunto y darle un nombre de archivo
            adjunto.add_header('Content-Disposition', 'attachment', filename=nombre_archivo)
            # Adjunta el archivo al mensaje
            mensaje.attach(adjunto)

        print(f"Intentando enviar correo a: {destinatario} con adjunto: {nombre_archivo}")
        # Inicia una conexión segura con el servidor SMTP de Gmail
        with smtplib.SMTP(SERVIDOR_SMTP, PUERTO_SMTP) as servidor:
            servidor.starttls()  # Habilita el cifrado TLS para una comunicación segura
            servidor.login(USUARIO_GMAIL, CONTRASEÑA_APP_GMAIL) # Inicia sesión con tus credenciales
            servidor.send_message(mensaje) # Envía el correo
        print(f"Correo enviado exitosamente a: {destinatario}")
        return True, f"Correo enviado exitosamente a: {destinatario}"
    except smtplib.SMTPAuthenticationError:
        # Error específico si las credenciales son incorrectas o la contraseña de aplicación no es válida
        print("ERROR: Autenticación SMTP fallida. Verifica usuario y contraseña de aplicación.")
        return False, "Error de autenticación: Verifica tu usuario de Gmail y tu contraseña de aplicación."
    except Exception as e:
        # Captura cualquier otro error durante el proceso de envío
        print(f"ERROR: Fallo al enviar el correo: {e}")
        return False, f"Error al enviar el correo: {e}"

@app.route('/')
def index():
    """
    Renderiza la página principal de la aplicación web.
    El HTML completo está incrustado aquí para simplificar la distribución del código.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Enviar Documento por Correo</title>
        <!-- Enlace a Tailwind CSS CDN para estilos rápidos y responsivos -->
        <script src="https://cdn.tailwindcss.com"></script>
        <!-- Enlace a la fuente Inter de Google Fonts para un aspecto moderno -->
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            /* Estilos generales para el cuerpo y el contenedor principal */
            body {
                font-family: 'Inter', sans-serif;
                background-color: #f0f2f5; /* Un gris claro para el fondo */
            }
            .container {
                max-width: 90%; /* Ancho máximo para el contenedor principal */
                margin: 2rem auto; /* Margen superior/inferior y centrado horizontal */
                padding: 1.5rem; /* Relleno interno */
                background-color: #ffffff; /* Fondo blanco para el contenido */
                border-radius: 1rem; /* Esquinas redondeadas */
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1); /* Sombra sutil */
            }
            /* Estilos base para los botones */
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 0.75rem 1.5rem;
                border-radius: 0.75rem;
                font-weight: 600; /* Texto seminegrita */
                transition: all 0.2s ease-in-out; /* Transición suave para efectos hover */
                cursor: pointer;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1); /* Sombra para profundidad */
            }
            /* Estilos para el botón principal (azul) */
            .btn-primary {
                background-color: #4f46e5; /* Azul índigo */
                color: white;
            }
            .btn-primary:hover {
                background-color: #4338ca; /* Azul índigo más oscuro al pasar el ratón */
                transform: translateY(-2px); /* Efecto de "levantar" al pasar el ratón */
            }
            /* Estilos para los botones secundarios (gris) */
            .btn-secondary {
                background-color: #6b7280; /* Gris */
                color: white;
            }
            .btn-secondary:hover {
                background-color: #4b5563; /* Gris más oscuro al pasar el ratón */
                transform: translateY(-2px);
            }
            /* Estilos para los campos de entrada de texto */
            .input-field {
                width: 100%;
                padding: 0.75rem 1rem;
                border: 1px solid #cbd5e1; /* Borde gris claro */
                border-radius: 0.75rem;
                font-size: 1rem;
                box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05); /* Sombra interna para efecto de profundidad */
            }
            .input-field:focus {
                outline: none; /* Elimina el contorno de enfoque predeterminado del navegador */
                border-color: #6366f1; /* Borde azul al enfocar */
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2); /* Sombra de enfoque azul */
            }
            /* Estilos para el cuadro de mensajes (éxito/error) */
            .message-box {
                padding: 1rem;
                border-radius: 0.75rem;
                margin-top: 1rem;
                font-weight: 500;
            }
            .message-success {
                background-color: #d1fae5; /* Verde claro */
                color: #065f46; /* Verde oscuro */
            }
            .message-error {
                background-color: #fee2e2; /* Rojo claro */
                color: #991b1b; /* Rojo oscuro */
            }
            /* Estilos para el spinner de carga */
            .loading-spinner {
                border: 4px solid rgba(255, 255, 255, 0.3);
                border-top: 4px solid #ffffff; /* Color del spinner */
                border-radius: 50%;
                width: 24px;
                height: 24px;
                animation: spin 1s linear infinite; /* Animación de giro */
                margin-right: 0.5rem;
            }
            /* Definición de la animación de giro */
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body class="flex items-center justify-center min-h-screen">
        <div class="container p-6 md:p-8 lg:p-10 w-full max-w-xl">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">Enviar Documento por Correo</h1>

            <div class="space-y-6">
                <!-- Sección de Subida de Archivo -->
                <div class="bg-gray-50 p-4 rounded-xl shadow-inner border border-gray-200">
                    <h2 class="text-xl font-semibold text-gray-700 mb-4">1. Seleccionar Archivo</h2>
                    <!-- Etiqueta personalizada para el input de archivo oculto -->
                    <label for="fileInput" class="btn btn-secondary w-full mb-4">
                        <!-- Icono de subir archivo -->
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                        Subir Archivo
                    </label>
                    <!-- El input acepta cualquier tipo de archivo (*/*) -->
                    <input type="file" id="fileInput" accept="*/*" class="hidden">
                    <!-- Muestra el nombre del archivo seleccionado -->
                    <p id="fileNameDisplay" class="text-gray-600 text-sm text-center"></p>
                </div>

                <!-- Sección de Envío de Correo -->
                <div class="bg-gray-50 p-4 rounded-xl shadow-inner border border-gray-200">
                    <h2 class="text-xl font-semibold text-gray-700 mb-4">2. Enviar Correo</h2>
                    <div class="mb-4">
                        <label for="recipientEmail" class="block text-gray-700 text-sm font-bold mb-2">Correo de Destino:</label>
                        <input type="email" id="recipientEmail" placeholder="ejemplo@dominio.com" class="input-field" required>
                    </div>
                    <div class="mb-6">
                        <label for="messageBody" class="block text-gray-700 text-sm font-bold mb-2">Mensaje (opcional):</label>
                        <textarea id="messageBody" rows="3" placeholder="Escribe tu mensaje aquí..." class="input-field resize-y"></textarea>
                    </div>
                    <button id="sendEmailButton" class="btn btn-primary w-full" disabled>
                        <!-- Spinner de carga que se muestra durante el envío -->
                        <span id="loadingSpinner" class="loading-spinner hidden"></span>
                        <span id="buttonText">Enviar Correo con Archivo</span>
                    </button>
                    <!-- Cuadro para mostrar mensajes de éxito o error -->
                    <div id="messageBox" class="message-box hidden"></div>
                </div>
            </div>
        </div>

        <script>
            // Obtener referencias a los elementos del DOM
            const fileInput = document.getElementById('fileInput');
            const fileNameDisplay = document.getElementById('fileNameDisplay');
            const recipientEmailInput = document.getElementById('recipientEmail');
            const messageBodyInput = document.getElementById('messageBody');
            const sendEmailButton = document.getElementById('sendEmailButton');
            const messageBox = document.getElementById('messageBox');
            const loadingSpinner = document.getElementById('loadingSpinner');
            const buttonText = document.getElementById('buttonText'); // Referencia al texto del botón

            let fileDataBase64 = null; // Variable para almacenar los datos del archivo en formato base64
            let attachedFileName = null; // Variable para almacenar el nombre del archivo adjunto

            // --- Funciones de Utilidad ---

            /**
             * Muestra un mensaje en el cuadro de mensajes de la interfaz.
             * @param {string} type - 'success' o 'error' para aplicar estilos.
             * @param {string} text - El texto del mensaje a mostrar.
             */
            function showMessage(type, text) {
                messageBox.classList.remove('hidden', 'message-success', 'message-error');
                messageBox.classList.add(type === 'success' ? 'message-success' : 'message-error');
                messageBox.textContent = text;
            }

            /**
             * Oculta y limpia el cuadro de mensajes.
             */
            function clearMessage() {
                messageBox.classList.add('hidden');
                messageBox.textContent = '';
            }

            /**
             * Habilita o deshabilita el botón de enviar correo
             * dependiendo de si hay un destinatario y un archivo adjunto.
             */
            function enableSendButton() {
                if (recipientEmailInput.value && fileDataBase64) {
                    sendEmailButton.disabled = false;
                } else {
                    sendEmailButton.disabled = true;
                }
            }

            /**
             * Resetea el estado de los datos del archivo y la interfaz de selección.
             */
            function resetAttachmentState() {
                fileInput.value = ''; // Limpiar la selección de archivo
                fileNameDisplay.textContent = ''; // Limpiar el nombre del archivo
                fileDataBase64 = null; // Resetear los datos del archivo
                attachedFileName = null; // Resetear el nombre del archivo
                enableSendButton(); // Re-evaluar el estado del botón de enviar
            }

            // --- Lógica de Subida de Archivo ---

            /**
             * Maneja la selección de archivos por parte del usuario.
             * Lee el archivo seleccionado y lo convierte a base64.
             */
            fileInput.addEventListener('change', (event) => {
                clearMessage();
                const file = event.target.files[0]; // Obtiene el primer archivo seleccionado
                if (file) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        fileDataBase64 = e.target.result; // Los datos del archivo en base64 (incluye el prefijo MIME)
                        attachedFileName = file.name; // El nombre original del archivo
                        fileNameDisplay.textContent = `Archivo seleccionado: ${file.name}`;
                        console.log("Archivo cargado. Longitud de fileDataBase64:", fileDataBase64 ? fileDataBase64.length : 0, "Nombre de archivo:", attachedFileName);
                        enableSendButton(); // Re-evaluar el estado del botón de enviar
                    };
                    reader.onerror = (e) => {
                        console.error("Error de FileReader:", reader.error);
                        showMessage('error', 'Error al leer el archivo. Intenta de nuevo.');
                        resetAttachmentState(); // Limpiar estado en caso de error
                    };
                    reader.readAsDataURL(file); // Lee el archivo como una URL de datos (base64)
                } else {
                    // Si no se selecciona ningún archivo (ej. el usuario abre el diálogo y lo cancela)
                    console.log("No se seleccionó ningún archivo.");
                    resetAttachmentState(); // Limpiar estado si no se elige archivo
                }
            });

            // --- Lógica del Formulario de Envío ---

            // Escucha cambios en el campo de correo para habilitar/deshabilitar el botón de enviar
            recipientEmailInput.addEventListener('input', enableSendButton);

            /**
             * Maneja el clic en el botón de enviar correo.
             * Recopila los datos y los envía al backend de Flask.
             */
            sendEmailButton.addEventListener('click', async () => {
                clearMessage(); // Limpiar mensajes anteriores
                const recipientEmail = recipientEmailInput.value;
                const messageBody = messageBodyInput.value;

                // Validaciones básicas en el frontend
                if (!recipientEmail) {
                    showMessage('error', 'Por favor, ingresa el correo del destinatario.');
                    return;
                }
                if (!fileDataBase64) {
                    showMessage('error', 'Por favor, selecciona un archivo para enviar.');
                    return;
                }

                // Deshabilitar el botón y mostrar el spinner de carga
                sendEmailButton.disabled = true;
                loadingSpinner.classList.remove('hidden');
                buttonText.classList.add('hidden'); // Ocultar texto del botón

                try {
                    // Envía los datos al endpoint /send_email del servidor Flask
                    const response = await fetch('/send_email', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            recipient: recipientEmail,
                            message: messageBody,
                            file_data: fileDataBase64, // Los datos del archivo en base64
                            file_name: attachedFileName // El nombre del archivo
                        })
                    });

                    const result = await response.json(); // Obtiene la respuesta JSON del servidor

                    if (result.success) {
                        showMessage('success', result.message);
                        // Limpiar campos y estado después de un envío exitoso
                        recipientEmailInput.value = '';
                        messageBodyInput.value = '';
                        resetAttachmentState(); // Resetear todo el estado de adjuntos
                    } else {
                        showMessage('error', result.message);
                    }
                } catch (error) {
                    console.error('Error al enviar el correo:', error);
                    showMessage('error', 'Error de conexión al servidor. Inténtalo de nuevo.');
                } finally {
                    // Restaurar el estado del botón y ocultar el spinner
                    loadingSpinner.classList.add('hidden');
                    buttonText.classList.remove('hidden'); // Mostrar texto del botón
                    enableSendButton(); // Re-evaluar el estado del botón
                }
            });

            // Comprobación inicial del estado del botón de enviar al cargar la página
            enableSendButton();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/send_email', methods=['POST'])
def handle_send_email():
    """
    Maneja la solicitud POST enviada desde el frontend para enviar el correo electrónico.
    """
    print("\n--- Solicitud POST recibida en /send_email ---")
    data = request.get_json() # Obtiene los datos JSON enviados desde el frontend
    destinatario = data.get('recipient')
    mensaje = data.get('message', '') # Mensaje opcional, por defecto cadena vacía
    archivo_data = data.get('file_data') # Los datos del archivo en base64
    nombre_archivo = data.get('file_name') # El nombre del archivo

    print(f"Destinatario: {destinatario}")
    print(f"Nombre del archivo: {nombre_archivo}")
    print(f"Longitud de datos del archivo (Base64): {len(archivo_data) if archivo_data else 0}")

    # Validaciones en el backend
    if not destinatario:
        print("Validación fallida: Correo de destino ausente.")
        return jsonify({"success": False, "message": "Correo de destino es requerido."}), 400
    if not archivo_data or not nombre_archivo:
        print("Validación fallida: Datos o nombre del archivo adjunto ausentes.")
        return jsonify({"success": False, "message": "No se ha proporcionado ningún archivo adjunto."}), 400

    asunto = f"Archivo Adjunto desde la Aplicación Web Python - {nombre_archivo}" # Asunto predeterminado
    # Llama a la función para enviar el correo con el archivo
    exito, mensaje_respuesta = enviar_correo_con_adjunto(destinatario, asunto, mensaje, archivo_data, nombre_archivo)

    if exito:
        print("Envío de correo exitoso.")
        return jsonify({"success": True, "message": mensaje_respuesta}), 200
    else:
        print("Envío de correo fallido.")
        return jsonify({"success": False, "message": mensaje_respuesta}), 500 # Código de error del servidor

if __name__ == '__main__':
    # Ejecuta la aplicación Flask.
    # debug=True es útil para el desarrollo (recarga automática, mensajes de error detallados).
    # Desactívalo (debug=False) en un entorno de producción.
    app.run(debug=True)


