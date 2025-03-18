from flet import *
import cv2
import os
import base64

# Función para convertir la imagen a Base64
def to_base64(image):
    _, buffer = cv2.imencode(".jpg", image)  # Codificar la imagen en formato JPEG
    return base64.b64encode(buffer).decode("utf-8")  # Convertir a Base64 y decodificar a string

# Función para acceder a la cámara
def access_camera(page: Page):
    # Crear un objeto VideoCapture para acceder a la cámara
    cap = cv2.VideoCapture(0)

    # Leer un fotograma de la cámara
    ret, frame = cap.read()

    if ret:
        # Convertir el fotograma a Base64
        image_base64 = to_base64(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Crear un objeto Image de Flet y mostrarlo en la página
        image = Image(src_base64=image_base64)
        page.add(image)

    # Liberar la cámara
    cap.release()
    cv2.destroyAllWindows()

# Función principal
def main(page: Page):
    # Verificar si la app se ejecuta en Android
    if not os.environ.get("ANDROID_SDK"):
        page.add(Text("Please run this app on an Android device."))
        return

    # Verificar y solicitar permiso de la cámara
    if not page.android_permission_status("CAMERA"):
        page.android_request_permission("CAMERA")

    # Función que se ejecuta cuando se concede el permiso
    def on_permission(permission: str):
        if permission == "CAMERA":
            access_camera(page)

    # Botón para acceder a la cámara
    button = ElevatedButton("Access Camera", on_click=lambda _: access_camera(page))
    page.add(button)

# Ejecutar la app
app(target=main)
