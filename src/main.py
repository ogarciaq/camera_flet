import os
from jnius import autoclass, cast
import flet as ft

def main(page: ft.Page):
    page.title = "Cámara Flet - Guardar en Galería"

    def abrir_camara(e):
        activity = autoclass("org.kivy.android.PythonActivity").mActivity

        # Clases de Android necesarias
        Intent = autoclass('android.content.Intent')
        MediaStore = autoclass('android.provider.MediaStore')
        File = autoclass('java.io.File')
        FileProvider = autoclass('androidx.core.content.FileProvider')
        Uri = autoclass('android.net.Uri')
        Environment = autoclass('android.os.Environment')
        ContentValues = autoclass('android.content.ContentValues')

        # Directorio público DCIM
        dcim_dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM).getAbsolutePath()
        image_path = os.path.join(dcim_dir, "foto_flet.jpg")
        photo_file = File(image_path)

        # Obtener URI segura con FileProvider
        authority = f"{activity.getPackageName()}.provider"
        photo_uri = FileProvider.getUriForFile(activity, authority, photo_file)

        # Crear Intent para la cámara
        intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        intent.putExtra(MediaStore.EXTRA_OUTPUT, photo_uri)

        if intent.resolveActivity(activity.getPackageManager()) is not None:
            activity.startActivityForResult(intent, 1888)
            page.add(ft.Text(f"Imagen guardada en la galería: {image_path}"))

            # Registrar la imagen en la galería
            content_resolver = activity.getContentResolver()
            values = ContentValues()
            values.put(MediaStore.Images.Media.TITLE, "Foto Flet")
            values.put(MediaStore.Images.Media.DESCRIPTION, "Foto tomada con Flet")
            values.put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg")
            values.put(MediaStore.Images.Media.DATA, image_path)
            content_resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values)
        else:
            page.add(ft.Text("Error: No se encontró una aplicación de cámara."))

    btn_camara = ft.ElevatedButton("Abrir Cámara", on_click=abrir_camara)
    page.add(btn_camara)

ft.app(target=main)
