# Miniature Adventure

API REST para la gestión de ofertas de trabajo entre estudiantes y empresas, permite a los usuarios, ya sean estudiantes o empresas, registrarse y utilizar la plataforma. Las empresas tienen la capacidad de crear, gestionar y eliminar ofertas de trabajo. Por otro lado, los estudiantes pueden visualizar, filtrar o postularse a las ofertas de trabajo disponibles.

## Tecnologías Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)![DRF](https://img.shields.io/badge/DRF-000000?style=for-the-badge&logo=django&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)![Shell](https://img.shields.io/badge/Shell-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)![TestsCase](https://img.shields.io/badge/TestsCase-000000?style=for-the-badge&logo=jest&logoColor=white)![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)![REST API](https://img.shields.io/badge/REST_API-005571?style=for-the-badge&logo=api&logoColor=white)![Railway](https://img.shields.io/badge/Deploy%20on%20Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)

## Tabla de Contenidos

- [Instalación](#instalación)
  - [Entorno con Docker](#entorno-con-docker)
  - [Entorno Local](#entorno-local)
- [API en vivo](#api-en-vivo)
- [Endpoints](#endpoints)
  - [Usurarios](#usuarios)
  - [Ofertas de Trabajo](#ofertas-de-trabajo)
  - [Postulaciones](#postulaciones)
- [Ejecutar Tests](#ejecutar-tests)
  - [Ejecutar tests en un entorno Docker](#ejecutar-tests-en-un-entorno-docker)
  - [Ejecutar tests en un entorno local](#ejecutar-tests-en-un-entorno-local)

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

3. **Configurar las variables de entorno:**
  
  Crea un archivo `.env` en la raíz del proyecto y configura las siguientes variables:
  
  - `SECRET_KEY` -> Clave secreta para la configuración de Django.
  - `DB_NAME` -> Nombre de la base de datos.
  - `DB_USER` -> Usuario de la base de datos.
  - `DB_PASSWORD` -> Contraseña del usuario de la base de datos.
  - `DB_HOST` -> Host de la base de datos.
  - `DB_PORT` -> Puerto de la base de datos.
  - `DJANGO_SETTINGS_MODULE` -> Módulo de configuración de Django.
  - `FRONTEND_URL` -> URL de verificación que se enviará por correo electrónico.
  - `CLOUDINARY_CLOUD_NAME` -> Nombre de la nube de Cloudinary.
  - `CLOUDINARY_API_KEY` -> Clave API de Cloudinary.
  - `CLOUDINARY_API_SECRET` -> Secreto API de Cloudinary.

### Entorno con Docker

**Requisitos:**
- Docker
- Docker Compose

1. **Actualizar las variables de entorno para la base de datos:**

  Actualiza las variables de entorno relacionadas con la base de datos creada con Docker:

  - `DB_NAME` -> Nombre de la base de datos.
  - `DB_USER` -> Usuario de la base de datos.
  - `DB_PASSWORD` -> Contraseña del usuario de la base de datos.
  - `DB_HOST` -> Host de la base de datos.
  - `DB_PORT` -> Puerto de la base de datos.

2. **Construir y ejecutar los contenedores:**

  ```bash
  docker compose --env-file .env -f docker/docker-compose.dev.yml up --build
  ```

¡Listo! El proyecto ahora debería estar en funcionamiento en tu entorno con Docker. Puedes acceder a él desde tu navegador web visitando `http://0.0.0.0:8000/`.

### Entorno Local

**Requisitos:**
- Python 3.x
- PostgreSQL

1. **Instalar las dependencias:**

  ```bash
  pip install -r requirements.txt
  ```

2. **Actualizar las variables de entorno para la base de datos:**

  Actualiza las variables de entorno de la base de datos con los datos correspondientes de tu entorno local:

  - `DB_NAME` -> Nombre de la base de datos.
  - `DB_USER` -> Usuario de la base de datos.
  - `DB_PASSWORD` -> Contraseña del usuario de la base de datos.
  - `DB_HOST` -> Host de la base de datos.
  - `DB_PORT` -> Puerto de la base de datos.

3. **Crear las migraciones:**

  ```bash
  python manage.py makemigrations --settings=config.settings.development
  python manage.py migrate --settings=config.settings.development
  ```

4. **Ejecutar el servidor:**

  ```bash
  python manage.py runserver --settings=config.settings.development
  ```

¡Listo! El proyecto ahora debería estar en funcionamiento en tu entorno local. Puedes acceder a él desde tu navegador web visitando `http://127.0.0.1:8000/`.

---

## API en vivo

El proyecto está desplegado en Railway, puedes acceder a la API en vivo aquí:

[![Producción](https://img.shields.io/badge/Production%20on%20Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)](https://miniature-adventure.johanngaviria.dev)

---

## Endpoints

### Usuarios

| Nombre | Método | URL | Descripción |
|:------ | :----- | :-- | :---------- |
| Registro de usuario | `POST` | `/api/users/register` | Endpoint para el registro de usuarios en la API. |
| Inicio de sesión del usuario | `POST` | `/api/users/login` | Endpoint para el inicio de sesión del usuarios en la API. |
| Cierre de sesión del usuario | `POST` | `/api/users/logout` | Endpoint para el cierre de sesión del usuario en la API. |
| Actualización de datos del usuario | `PUT` | `/api/users/update` | Endpoint para la actualización de datos del usuario en la API. |
| Eliminación de usuario | `DELETE` | `/api/users/delete` | Endpoint para la eliminación del usuario en la API. |
| Agregar datos del estudiante | `POST` | `/api/users/student/add` | Endpoint para agregar datos del estudiante en la API. |
| Obtener datos del estudiante | `GET` | `/api/users/student/get` | Endpoint para obtener datos del estudiante en la API. |
| Actualizar datos del estudiante | `PUT` | `/api/users/student/update` | Endpoint para actualizar datos del estudiante en la API. |
| Agregar datos de la compañia | `POST` | `/api/users/company/add` | Endpoint para agregar datos de la compañia en la API. |
| Obtener datos de la compañia | `GET` | `/api/users/company/get` | Endpoint para obtener datos de la compañia en la API. |
| Actualizar datos de la compañia | `PUT` | `/api/users/company/update` | Endpoint para actualizar datos de la compañia en la API. |

---

### Ofertas de trabajo

| Nombre | Método | URL | Descripción |
|:------ | :----- | :-- | :---------- |
| Crear oferta de trabajo | `POST` | `/api/job_offers/create` | Endpoint para crear una oferta de trabajo en la API. |
| Obtener oferta de trabajo | `GET` | `/api/job_offers/get/<job_offer_id>` | Endpoint para obtener una oferta de trabajo en la API. |
| Obtener todas las ofertas de trabajo | `GET` | `/api/job_offers/all` | Endpoint para obtener todas las ofertas de trabajo en la API. |
| Filtrar ofertas de trabajo | `GET` | `/api/job_offers/filter` | Endpoint para filtrar ofertas de trabajo en la API. |
| Actualizar oferta de trabajo | `PUT` | `/api/job_offers/update/<job_offer_id>` | Endpoint para actualizar una oferta de trabajo en la API. |
| Cerrar oferta de trabajo | `PUT` | `/api/job_offers/close/<job_offer_id>` | Endpoint para cerrar una oferta de trabajo en la API. |
| Eliminar oferta de trabajo | `DELETE` | `/api/job_offers/delete/<job_offer_id>` | Endpoint para eliminar una oferta de trabajo en la API. |

---

### Postulaciones

| Nombre | Método | URL | Descripción |
|:------ | :----- | :-- | :---------- |
| Postularse a una oferta de trabajo | `POST` | `/api/postulations/postulate/<job_offer_id>` | Endpoint para postularse a una oferta de trabajo en la API. |
| Retirar postulación a una oferta de trabajo | `DELETE` | `/api/postulations/withdraw/<job_offer_id>` | Endpoint para retirar la postulación a una oferta de trabajo en la API. |
| Obtener postulaciones a una oferta de trabajo | `GET` | `/api/postulations/get/<job_offer_id>` | Endpoint para obtener las postulaciones a una oferta de trabajo en la API. |
| Aceptar o rechazar postulaciones a una oferta de trabajo | `POST` | `/api/postulations/accept_reject/<job_offer_id>` | Endpoint para aceptar o rechazar postulaciones a una oferta de trabajo en la API. |

---

## Ejecutar Tests  

### Ejecutar tests en un entorno Docker

- **Ejecutar todos los tests:**  
  
  ```bash
  docker exec -it <id_container> python manage.py test apps --settings=config.settings.development
  ```

- **Ejecutar un test específico:**  
  
  ```bash
  docker exec -it <id_container> python manage.py test apps.<nombre_módulo>.tests.<nombre_test> --settings=config.settings.development
  ```  

  Reemplaza `<nombre_módulo>` y `<nombre_test>` con los valores correspondientes.  

### Ejecutar tests en un entorno local

- **Ejecutar todos los tests:**  
  
  ```bash
  python manage.py test apps --settings=config.settings.development
  ```

- **Ejecutar un test específico:**  
  ```bash
  python manage.py test apps.<nombre_módulo>.tests.<nombre_test> --settings=config.settings.development
  ```
  Reemplaza `<nombre_módulo>` y `<nombre_test>` con los valores correspondientes.
