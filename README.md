# Miniature Adventure

Desarrollo de una API REST para la gestión de ofertas de trabajo entre estudiantes y empresas, permite a los usuarios, ya sean estudiantes o empresas, registrarse y utilizar la plataforma. Las empresas tienen la capacidad de crear, gestionar y eliminar ofertas de trabajo, así como dejar comentarios sobre los estudiantes seleccionados para sus vacantes. Por otro lado, los estudiantes pueden postularse a las ofertas disponibles, y también tienen la posibilidad de dejar comentarios sobre su experiencia con las ofertas de trabajo a las que se han postulado o en las que han sido seleccionados.

## Tecnologías Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## Tabla de Contenidos

- [Instalación](#instalación)
  - [Entorno con Docker](#entorno-con-docker)
  - [Entorno Local](#entorno-local)

## Instalación

### Pasos de Instalación

1. **Clona este repositorio:**

```bash
git clone https://github.com/JohannGaviria/miniature-adventure.git
cd miniature-adventure
```

2. **Crea el entorno virtual:**

Utiliza `venv` o cualquier otro gestor de entornos virtuales. Luego, crea y activa el entorno virtual:

```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Mac/Linux
source venv/bin/activate
```

3. **Crea las variables de entorno:**
- Crea un archivo `.env` en la raíz del proyecto y configura las siguientes variables:
  - `SECRET_KEY` -> Clave secreta para la configuración de Django.
  - `DB_NAME` -> Nombre de la base de datos.
  - `DB_USER` -> Usuario de la base de datos.
  - `DB_PASSWORD` -> Contraseña del usuario de la base de datos.
  - `DB_HOST` -> Host de la base de datos.
  - `DB_PORT` -> Puerto de la base de datos.
  - `DJANGO_SETTINGS_MODULE` -> Módulo de configuración de Django.
  - `EMAIL_HOST_USER` -> Correo electrónico para el envío de notificaciones por email.
  - `EMAIL_HOST_PASSWORD` -> Contraseña del correo electrónico.
  - `SECURITY_PASSWORD_SALT` -> Contraseña segura que permitirá al módulo `itsdangerous` generar y verificar tokens de forma segura.
  - `FRONTEND_URL` -> URL de verificación que se enviará por correo electrónico.

### Entorno con Docker

**Requisitos:**
- Docker
- Docker Compose

1. **Construir y ejecutar los contenedores:**

```bash
docker compose -f docker/docker-compose.dev.yml build
docker compose -f docker/docker-compose.dev.yml up
```

¡Listo! El proyecto ahora debería estar en funcionamiento en tu entorno con docker. Puedes acceder a él desde tu navegador web visitando `http://0.0.0.0:8000/`.

### Entorno Local

**Requisitos:**
- Python
- PostgreSQL

1. **Instalar las dependencias:**

```bash
pip install -r requirements.txt
```

2. **Crea las migraciones:**

```bash
python manage.py makemigrations --settings=config.settings.development
python manage.py migrate --settings=config.settings.development
```

3. **Ejecutar el servidor:**

```bash
python manage.py runserver --settings=config.settings.development
```

¡Listo! El proyecto ahora debería estar en funcionamiento en tu entorno local. Puedes acceder a él desde tu navegador web visitando `http://127.0.0.1:8000/`.

---
