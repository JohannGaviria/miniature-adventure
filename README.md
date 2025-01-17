# Miniature Adventure

Desarrollo de una API REST para la gestión de ofertas de trabajo entre estudiantes y empresas, permite a los usuarios, ya sean estudiantes o empresas, registrarse y utilizar la plataforma. Las empresas tienen la capacidad de crear, gestionar y eliminar ofertas de trabajo, así como dejar comentarios sobre los estudiantes seleccionados para sus vacantes. Por otro lado, los estudiantes pueden postularse a las ofertas disponibles, y también tienen la posibilidad de dejar comentarios sobre su experiencia con las ofertas de trabajo a las que se han postulado o en las que han sido seleccionados.

## Tecnologías Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)![DRF](https://img.shields.io/badge/DRF-000000?style=for-the-badge&logo=django&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)![Shell](https://img.shields.io/badge/Shell-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)![Tests](https://img.shields.io/badge/Tests-000000?style=for-the-badge&logo=jest&logoColor=white)![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)


## Tabla de Contenidos

- [Instalación](#instalación)
  - [Entorno con Docker](#entorno-con-docker)
  - [Entorno Local](#entorno-local)
- [Endpoints](#endpoints)
  - [Usurarios](#usuarios)
  - [Ofertas de Trabajo](#ofertas-de-trabajo)

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
  - `FRONTEND_URL` -> URL de verificación que se enviará por correo electrónico.
  - `CLOUDINARY_CLOUD_NAME` -> Nombre de la nube de Cloudinary.
  - `CLOUDINARY_API_KEY` -> Clave API de Cloudinary.
  - `CLOUDINARY_API_SECRET` -> Secreto API de Cloudinary.

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

## Endpoints

[![Postman](https://img.shields.io/badge/Ver-Documentacion-FF6C37?style=for-the-badge&logo=postman&logoColor=white)](https://documenter.getpostman.com/view/38982911/2sAYQZGrs8)

### Usuarios

| Nombre | Método | URL | Descripción |
|:------ | :----- | :-- | :---------- |
| [Registro de usuario](#registro-de-usuario) | `POST` | `/api/users/register` | Endpoint para el registro de usuarios en la API. |
| [Inicio de sesión del usuario](#inicio-de-sesión-del-usuario) | `POST` | `/api/users/login` | Endpoint para el inicio de sesión del usuarios en la API. |
| [Cierre de sesión del usuario](#cierre-de-sesión-del-usuario) | `POST` | `/api/users/logout` | Endpoint para el cierre de sesión del usuario en la API. |
| [Actualización de datos del usuario](#actualización-de-datos-del-usuario) | `PUT` | `/api/users/update` | Endpoint para la actualización de datos del usuario en la API. |
| [Eliminación de usuario](#eliminación-de-usuario) | `DELETE` | `/api/users/delete` | Endpoint para la eliminación del usuario en la API. |
| [Agregar datos del estudiante](#agregar-datos-del-estudiante) | `POST` | `/api/users/student/add` | Endpoint para agregar datos del estudiante en la API. |
| [Obtener datos del estudiante](#obtener-datos-del-estudiante) | `GET` | `/api/users/student/get` | Endpoint para obtener datos del estudiante en la API. |
| [Actualizar datos del estudiante](#actualizar-datos-del-estudiante) | `PUT` | `/api/users/student/update` | Endpoint para actualizar datos del estudiante en la API. |
| [Agregar datos de la compañia](#agregar-datos-de-la-compañia) | `POST` | `/api/users/company/add` | Endpoint para agregar datos de la compañia en la API. |
| [Obtener datos de la compañia](#obtener-datos-de-la-compañia) | `GET` | `/api/users/company/get` | Endpoint para obtener datos de la compañia en la API. |
| [Actualizar datos de la compañia](#actualizar-datos-de-la-compañia) | `PUT` | `/api/users/company/update` | Endpoint para actualizar datos de la compañia en la API. |

#### Registro de usuario

##### Método HTTP

```http
POST /api/users/register
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Requerido**. Nombre del usuario |
| `first_name` | `string` | **Requerido**. Primer nombre del usuario |
| `last_name` | `string` | **Opcional**. Apellido del usuario |
| `email` | `string` | **Requerido**. Correo electrónico del usuario |
| `password` | `string` | **Requerido**. Contraseña del usuario |
| `user_type` | `string` | **Requerido**. Tipo de usuario |

> **NOTA**: El parámetro `user_type` solo acepta los siguientes valores:
>
> - **student**: Indica que el usuario es un estudiante.
> - **company**: Indica que el usuario es una empresa.

##### Ejemplo de solicitud

```http
Content-Type: application/json

{
  "username": "testUsername",
  "first_name": "test first name",
  "last_name": "test last name",
  "email": "test@email.com",
  "password": "testPassword"
  "user_type": "student"
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "status": "success",
  "message": "User registered successfully"
}
```

#### Inicio de sesión del usuario

##### Método HTTP

```http
POST /api/users/login
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `email`   | `string` | **Requerido**. Correo electrónico del usuario |
| `password`| `string` | **Requerido**. Contraseña del usuario |

##### Ejemplo de solicitud

```http
Content-Type: application/json

{
  "email": "test@email.com",
  "password": "testPassword"
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
  "status": "success",
  "message": "User logged in successfully.",
  "data": {
    "token": {
      "token_key": "your_token_key",
      "token_expiration": "2023-10-10T10:00:00Z"
    },
    "user": {
      "id": 1,
      "username": "testUsername",
      "first_name": "test first name",
      "last_name": "test last name",
      "email": "test@email.com",
      "user_type": "student",
      "date_joined": "2025-01-03T04:07:05.726101Z",
      "last_login": null
    }
  }
}
```

#### Cierre de sesión del usuario

##### Método HTTP

```http
POST /api/users/logout
```

##### Headers

| Header           | Tipo     | Descripción                |
| :--------------- | :------- | :------------------------- |
| `Authorization`  | `string` | **Requerido**. Token de autenticación del usuario |

##### Ejemplo de solicitud

```http
Authorization: Token <your_token_key>
Content-Type: application/json
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "User logged out successfully."
}
```

#### Actualización de datos del usuario

##### Método HTTP

```http
PUT /api/users/update
```

##### Headers

| Header           | Tipo     | Descripción                |
| :--------------- | :------- | :------------------------- |
| `Authorization`  | `string` | **Requerido**. Token de autenticación del usuario |

##### Parámetros

| Parámetro     | Tipo     | Descripción                |
| :------------ | :------- | :------------------------- |
| `first_name`  | `string` | **Opcional**. Primer nombre del usuario |
| `last_name`   | `string` | **Opcional**. Apellido del usuario |
| `email`       | `string` | **Opcional**. Correo electrónico del usuario |
| `password`    | `string` | **Opcional**. Contraseña del usuario |
| `user_type`   | `string` | **Opcional**. Tipo de usuario |

##### Ejemplo de solicitud

```http
Authorization: Token your_token_key
Content-Type: application/json

{
  "first_name": "UpdatedFirstName",
  "last_name": "UpdatedLastName"
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "User data updated successfully.",
  "data": {
    "token": {
      "token_key": "your_new_token_key",
      "token_expiration": "2025-01-06T22:50:19.554753+00:00"
    },
    "user": {
      "id": 1,
      "username": "testUsername",
      "first_name": "UpdatedFirstName",
      "last_name": "UpdatedLastName",
      "email": "test@email.com",
      "user_type": "student",
      "date_joined": "2025-01-03T04:07:05.726101Z",
      "last_login": "2025-01-03T23:09:15.534885Z"
    }
  }
}
```

#### Eliminación de usuario

##### Método HTTP

```http
DELETE /api/users/delete
```

##### Headers

| Header           | Tipo     | Descripción                |
| :--------------- | :------- | :------------------------- |
| `Authorization`  | `string` | **Requerido**. Token de autenticación del usuario |

##### Ejemplo de solicitud

```http
Authorization: Token your_token_key
Content-Type: application/json
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "User deleted successfully."
}
```

#### Agregar datos del estudiante

##### Método HTTP

```http
POST /api/users/student/add
```

##### Headers

| Header           | Tipo     | Descripción                |
| :--------------- | :------- | :------------------------- |
| `Authorization`  | `string` | **Requerido**. Token de autenticación del usuario |

##### Parámetros

| Parámetro                 | Tipo     | Descripción                |
| :------------------------ | :------- | :------------------------- |
| `university`              | `string` | **Requerido**. Universidad del estudiante |
| `degree`                  | `string` | **Requerido**. Título del estudiante |
| `major`                   | `string` | **Requerido**. Especialidad del estudiante |
| `graduation_year`         | `integer`| **Requerido**. Año de graduación del estudiante |
| `professional_experience` | `string` | **Requerido**. Experiencia profesional del estudiante |
| `cv`                      | `file`   | **Opcional**. Archivo de curriculum vitae del estudiante |
| `about_me`                | `string` | **Requerido**. Información sobre el estudiante |

##### Ejemplo de solicitud

```http
Authorization: Token your_token_key
Content-Type: application/json

{
  "university": "Test University",
  "degree": "Test Degree",
  "major": "Test Major",
  "graduation_year": 2025,
  "professional_experience": "Test Experience",
  "about_me": "Test About Me"
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "status": "success",
  "message": "Student data added successfully."
}
```

#### Obtener datos del estudiante

##### Método HTTP

```http
GET /api/users/student/get
```

##### Headers

| Header           | Tipo     | Descripción                |
| :--------------- | :------- | :------------------------- |
| `Authorization`  | `string` | **Requerido**. Token de autenticación del usuario |

##### Ejemplo de solicitud

```http
Authorization: Token your_token_key
Content-Type: application/json
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "Student data was successfully obtained.",
  "data": {
    "student": {
      "id": 1,
      "university": "Test University",
      "degree": "Test Degree",
      "major": "Test Major",
      "graduation_year": 2025,
      "professional_experience": "Test Experience",
      "about_me": "Test About Me",
      "cv": "https://res.cloudinary.com/dccnkrmty/image/upload/v1736292828/miniature-adventure/students_cvs/test_cv.pdf",
      "user": 1
    }
  }
}
```

#### Actualizar datos del estudiante

##### Método HTTP

```http
PUT /api/users/student/update
```

##### Headers

| Header           | Tipo     | Descripción                |
| :--------------- | :------- | :------------------------- |
| `Authorization`  | `string` | **Requerido**. Token de autenticación del usuario |

##### Parámetros

| Parámetro                 | Tipo     | Descripción                |
| :------------------------ | :------- | :------------------------- |
| `university`              | `string` | **Opcional**. Universidad del estudiante |
| `degree`                  | `string` | **Opcional**. Título del estudiante |
| `major`                   | `string` | **Opcional**. Especialidad del estudiante |
| `graduation_year`         | `integer`| **Opcional**. Año de graduación del estudiante |
| `professional_experience` | `string` | **Opcional**. Experiencia profesional del estudiante |
| `cv`                      | `file`   | **Opcional**. Archivo de curriculum vitae del estudiante |
| `about_me`                | `string` | **Opcional**. Información sobre el estudiante |

##### Ejemplo de solicitud

```http
Authorization: Token your_token_key
Content-Type: application/json

{
  "university": "Updated University",
  "degree": "Updated Degree",
  "major": "Updated Major",
  "graduation_year": 2026,
  "professional_experience": "Updated Experience",
  "about_me": "Updated About Me"
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "Student data updated successfully."
}
```

#### Agregar datos de la compañia

##### Método HTTP

```http
POST /api/users/company/add
```

##### Headers

| Header           | Tipo     | Descripción                |
| :--------------- | :------- | :------------------------- |
| `Authorization`  | `string` | **Requerido**. Token de autenticación del usuario |

##### Parámetros

| Parámetro                 | Tipo     | Descripción                |
| :------------------------ | :------- | :------------------------- |
| `name`                    | `string` | **Requerido**. Nombre de la compañia |
| `industry`                | `string` | **Requerido**. Industria de trabajo de la compañia |
| `location`                | `string` | **Requerido**. Ubicación de la empresa |
| `description`             | `string` | **Requerido**. Descripción de la empresa |

##### Ejemplo de solicitud

```http
Authorization: Token your_token_key
Content-Type: application/json

{
  "name": "Test Name Company",
  "industry": "Test Industry",
  "location": "Test Location",
  "description": "Test Description"
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "status": "success",
  "message": "Company data added successfully."
}
```

#### Obtener datos de la compañia

##### Método HTTP

```http
GET /api/users/company/get
```

##### Headers

| Header           | Tipo     | Descripción                |
| :--------------- | :------- | :------------------------- |
| `Authorization`  | `string` | **Requerido**. Token de autenticación del usuario |

##### Ejemplo de solicitud

```http
Authorization: Token your_token_key
Content-Type: application/json
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "Company data was successfully obtained.",
  "data": {
    "company": {
      "id": 1,
      "name": "Grant - Bogisich",
      "industry": "and Sons",
      "location": "tw",
      "description": "Principal",
      "user": 9
    }
  }
}
```

#### Agregar datos de la compañia

##### Método HTTP

```http
POST /api/users/company/add
```

##### Headers

| Header           | Tipo     | Descripción                |
| :--------------- | :------- | :------------------------- |
| `Authorization`  | `string` | **Requerido**. Token de autenticación del usuario |

##### Parámetros

| Parámetro                 | Tipo     | Descripción                |
| :------------------------ | :------- | :------------------------- |
| `name`                    | `string` | **Optional**. Nombre de la compañia |
| `industry`                | `string` | **Optional**. Industria de trabajo de la compañia |
| `location`                | `string` | **Optional**. Ubicación de la empresa |
| `description`             | `string` | **Optional**. Descripción de la empresa |

##### Ejemplo de solicitud

```http
Authorization: Token your_token_key
Content-Type: application/json

{
  "name": "Updated Name Company",
  "industry": "Updated Industry",
  "location": "Updated Location",
  "description": "Updated Description"
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 20o Ok
Content-Type: application/json

{
  "status": "success",
  "message": "Company data updated successfully."
}
```

---

### Ofertas de trabajo

| Nombre | Método | URL | Descripción |
|:------ | :----- | :-- | :---------- |
| [Crear oferta de trabajo](#crear-oferta-de-trabajo) | `POST` | `/api/job_offers/create` | Endpoint para crear una oferta de trabajo en la API. |

#### Crear oferta de trabajo

##### Método HTTP

```http
POST /api/job_offers/create
```

##### Headers

| Header           | Tipo     | Descripción                |
| :--------------- | :------- | :------------------------- |
| `Authorization`  | `string` | **Requerido**. Token de autenticación del usuario |

##### Parámetros

| Parámetro     | Tipo     | Descripción                |
| :------------ | :------- | :------------------------- |
| `title`       | `string` | **Requerido**. Título de la oferta de trabajo |
| `description` | `string` | **Opcional**. Descripción de la oferta de trabajo |
| `requirements`| `string` | **Opcional**. Requisitos de la oferta de trabajo |
| `location`    | `string` | **Requerido**. Ubicación de la oferta de trabajo |
| `salary`      | `integer`| **Opcional**. Salario de la oferta de trabajo |
| `work_mode`   | `string` | **Requerido**. Modalidad de trabajo (presencial, remoto, híbrido) |

> **NOTA**: El parámetro `work_mode` solo acepta los siguientes valores:
>
> - **remote**: Indica que el modo de trabajo de la oferta es remoto.
> - **onsite**: Indica que el modo de trabajo de la oferta es presencial.
> - **hybrid**: Indica que el modo de trabajo de la oferta es hibrido.

##### Ejemplo de solicitud

```http
Authorization: Token your_token_key
Content-Type: application/json

{
  "title": "Test Job Offer",
  "description": "Test Description",
  "requirements": "Test Requirement",
  "location": "Test Location",
  "salary": 50000,
  "work_mode": "hybrid",
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "status": "success",
  "message": "Job offer created successfully."
}
```

---
