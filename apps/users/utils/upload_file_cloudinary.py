import cloudinary.uploader


def upload_cv_to_cloudinary(cv_file):
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