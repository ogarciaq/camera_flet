import os
import flet as ft
from jnius import autoclass, cast

def main(page: ft.Page):
    page.title = "Aplicación Flet con Cámara"

    def abrir_camara(e):
        # Obtener la actividad principal de Android
        activity_host_class = os.getenv("MAIN_ACTIVITY_HOST_CLASS_NAME")
        assert activity_host_class
        activity_host = autoclass(activity_host_class)
        activity = activity_host.mActivity

        # Crear un archivo para la imagen
        Environment = autoclass('android.os.Environment')
        File = autoclass('java.io.File')
        storage_dir = activity.getExternalFilesDir(Environment.DIRECTORY_PICTURES)
        image_file = File.createTempFile('foto_', '.jpg', storage_dir)
        image_path = image_file.getAbsolutePath()

        # Obtener URI para el archivo utilizando FileProvider
        FileProvider = autoclass('androidx.core.content.FileProvider')
        context = cast('android.content.Context', activity.getApplicationContext())
        uri = FileProvider.getUriForFile(context, 'com.tu.paquete.fileprovider', image_file)

        # Intent para abrir la cámara
        Intent = autoclass('android.content.Intent')
        intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        intent.putExtra(MediaStore.EXTRA_OUTPUT, uri)
        activity.startActivityForResult(intent, 1)

        # Mostrar la ruta donde se guardará la imagen
        page.add(ft.Text(f"Imagen guardada en: {image_path}"))

    btn_camara = ft.ElevatedButton("Abrir Cámara", on_click=abrir_camara)
    page.add(btn_camara)

ft.app(target=main)
