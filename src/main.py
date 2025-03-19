import os
from jnius import autoclass
import flet as ft

def main(page: ft.Page):
    page.title = "Aplicación Flet con Cámara"

    def abrir_camara(e):
        # Obtener la clase Activity actual
        activity_host_class = os.getenv("MAIN_ACTIVITY_HOST_CLASS_NAME")
        assert activity_host_class
        activity_host = autoclass(activity_host_class)
        activity = activity_host.mActivity

        # Intent para abrir la cámara
        Intent = autoclass('android.content.Intent')
        MediaStore = autoclass('android.provider.MediaStore')
        CAMERA_REQUEST = 1888

        intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        activity.startActivityForResult(intent, CAMERA_REQUEST)

    btn_camara = ft.ElevatedButton("Abrir Cámara", on_click=abrir_camara)
    page.add(btn_camara)

ft.app(target=main)
