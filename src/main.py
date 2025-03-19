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

        # Clases de Android necesarias
        Intent = autoclass('android.content.Intent')
        MediaStore = autoclass('android.provider.MediaStore')
        File = autoclass('java.io.File')
        Environment = autoclass('android.os.Environment')
        Uri = autoclass('android.net.Uri')
        ContentValues = autoclass('android.content.ContentValues')

        # Directorio público DCIM (Galería)
        dcim_dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM).getAbsolutePath()
        image_path = os.path.join(dcim_dir, "foto_galeria.jpg")
        photo_file = File(image_path)

        # Crear un intent para abrir la cámara
        intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        intent.putExtra(MediaStore.EXTRA_OUTPUT, Uri.fromFile(photo_file))

        # Guardar la foto en la galería usando MediaStore
        def guardar_en_galeria():
            content_resolver = activity.getContentResolver()
            values = ContentValues()
            values.put(MediaStore.Images.Media.TITLE, "Foto Flet")
            values.put(MediaStore.Images.Media.DESCRIPTION, "Foto tomada con Flet")
            values.put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg")
            values.put(MediaStore.Images.Media.DATA, image_path)
            content_resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values)

        # Abrir la cámara
        activity.startActivityForResult(intent, 1888)

        # Agregar la imagen a la galería después de tomar la foto
        page.add(ft.Text(f"Imagen guardada en la galería: {image_path}"))
        guardar_en_galeria()

    btn_camara = ft.ElevatedButton("Abrir Cámara", on_click=abrir_camara)
    page.add(btn_camara)

ft.app(target=main)
