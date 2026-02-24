# ✈️ Travel Bucket List API (v2.0 - Edición Docker & DB)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Estado-Terminado-success?style=for-the-badge)

> **Práctica 3.1 - Desarrollo Web en Entorno Servidor**
> API REST profesional con persistencia en base de datos relacional, contenerizada y desplegada en la nube.

---

## 📋 Descripción del Proyecto

Esta evolución de la API de viajes deja atrás el almacenamiento volátil para implementar una arquitectura robusta basada en **PostgreSQL**. Permite gestionar destinos y actividades turísticas de forma persistente, con validación de datos estricta y control de versiones de la base de datos.

### 🌟 Mejoras de esta versión
* 🗄️ **Persistencia Real:** Migración total de listas de Python/SQLite a **PostgreSQL**.
* 🐳 **Contenerización:** Despliegue unificado mediante **Docker** y **Docker Compose**.
* 🔄 **Migraciones:** Gestión de esquemas de base de datos automatizada con **Alembic**.
* ☁️ **Cloud:** Despliegue continuo configurado en **Render**.
* 🔐 **Seguridad:** Gestión de credenciales mediante variables de entorno (`.env`).

---

## 🛠️ Tecnologías Utilizadas

* **Framework:** FastAPI
* **Base de Datos:** PostgreSQL
* **ORM:** SQLAlchemy
* **Migraciones:** Alembic
* **Contenedores:** Docker & Docker Compose
* **Entornos:** Python-Dotenv

---

## 🚀 Instalación y Puesta en Marcha (Local)

La forma más sencilla de ejecutar el proyecto es utilizando **Docker Desktop**:

### 1. Clonar el proyecto y configurar entorno
Crea un archivo `.env` en la raíz del proyecto con la siguiente configuración:
```env
DATABASE_URL=postgresql://app:12345678AZARQUIEL@localhost:5432/apiusers
ENV=development
````
### 2. Levantar los servicios
Ejecuta el siguiente comando para levantar la API y la Base de Datos automáticamente:

```bash
docker compose up --build
````
### 3. Aplicar Migraciones
Una vez levantados los contenedores, sincroniza las tablas de la base de datos para crear la estructura necesaria:

```bash
# Usando el entorno virtual local
python -m alembic upgrade head
````
🎉 **API disponible en:** [http://localhost:80/docs](http://localhost:80/docs)

---

## 🌐 Despliegue en Producción
El proyecto está desplegado y operativo en **Render**. La base de datos de producción se actualiza automáticamente mediante un comando de *Pre-deploy* que ejecuta **Alembic** antes de cada lanzamiento.

🔗 **URL del Proyecto:** [https://travel-bucket-list-apirest.onrender.com/docs](https://travel-bucket-list-apirest.onrender.com/docs)

---

## 🔌 Endpoints Destacados
Además de las operaciones CRUD habituales, la API gestiona relaciones y persistencia avanzada:

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| **GET** | `/destinations/` | Lista todos los destinos con sus actividades relacionadas. |
| **POST** | `/destinations/` | Crea un nuevo destino (Persistente en PostgreSQL). |
| **PUT** | `/destinations/{id}` | Actualización total de los datos de un destino. |
| **DELETE** | `/destinations/{id}` | Borrado físico del registro en la base de datos. |

---

## ⚙️ Estructura de Entornos
El sistema detecta automáticamente el contexto de ejecución para configurar la conexión:

* **Desarrollo:** Utiliza el archivo `.env` local y conecta a `localhost`.
* **Producción:** Utiliza las variables de entorno configuradas en el panel de **Render** para conectar a la base de datos interna.

---

<div align="center">
  <p>Realizado por <strong>Lucilene Vidal Lima</strong></p>
  <p>S2DAW - IES Azarquiel</p>
</div>


