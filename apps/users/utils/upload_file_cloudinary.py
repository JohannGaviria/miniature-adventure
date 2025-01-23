import cloudinary.uploader


def upload_cv_to_cloudinary(cv_file):
    """
    Sube un archivo a Cloudinary y retorna la URL del archivo subido.

    args:
        cv_file (File): Archivo a subir a Cloudinary.
    
    returns:
        str: URL del archivo subido a Cloudinary.
    
    raises:
        Exception: Error al subir el archivo a Cloudinary.
    """
    try:
        # Subir archivo a Cloudinary
        response = cloudinary.uploader.upload(
            cv_file,
            folder="miniature-adventure/students_cvs",
            resource_type="auto"
        )
        # Retornar la URL del archivo subido
        return response['secure_url']
    except Exception as e:
        # Retornar un error si no se pudo subir el archivo
        raise Exception(f"Error uploading file to Cloudinary: {str(e)}.")
