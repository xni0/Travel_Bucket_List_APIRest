# ✈️ Travel Bucket List API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Estado-Terminado-success?style=for-the-badge)

> **Práctica 3.1 - Desarrollo Web en Entorno Servidor** > Una API REST completa para gestionar tus destinos de viaje soñados, creada como base para futuros proyectos Frontend.

---

## 📋 Descripción del Proyecto

Este proyecto implementa una **API RESTful** utilizando el framework **FastAPI**. Simula un backend para una aplicación de viajes (**"Bucket List"**) donde los usuarios pueden gestionar ciudades que quieren visitar o que ya han visitado.

### 🌟 ¿Por qué este tema?
He elegido el dominio de **"Viajes"** porque permite una gran riqueza de datos visuales para el futuro desarrollo en la asignatura de *Desarrollo Web en Entorno Cliente (DWEC)*:
* ✅ **Booleanos:** Para marcar destinos como "Visitados" (checkboc).
* 💰 **Números:** Para cálculos de presupuestos totales.
* 📋 **Listas:** Para gestionar actividades turísticas por cada ciudad.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Framework:** FastAPI
* **Servidor:** Uvicorn
* **Validación de datos:** Pydantic

---

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

### 1. Clonar o descomprimir el proyecto
Ubícate en la carpeta del proyecto desde tu terminal.

### 2. Crear y activar el entorno virtual
Es recomendable usar un entorno aislado para instalar las dependencias.

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar dependencias

```bash
uvicorn main:app --reload
```
🎉 **¡Listo!** La API estará corriendo en: `http://127.0.0.1:8000`

---

## 📖 Documentación de la API

FastAPI genera documentación automática e interactiva. Una vez iniciado el servidor, visita cualquiera de estos enlaces en tu navegador:

* **Swagger UI (Recomendado):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
  *Permite probar los endpoints directamente desde el navegador.*
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔌 Endpoints Disponibles

La API cuenta con las operaciones CRUD completas:

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/destinations/` | Obtiene la lista completa de destinos. |
| `GET` | `/destinations/{id}` | Obtiene los detalles de un destino específico por su ID. |
| `POST` | `/destinations/` | Crea un nuevo destino (Valida que el ID no esté duplicado). |
| `PUT` | `/destinations/{id}` | Actualiza la información completa de un destino existente. |
| `DELETE` | `/destinations/{id}` | Elimina un destino de la lista. |

---

## 🧪 Pruebas

Se incluye un fichero llamado `test_api.rest`. 
Puedes utilizarlo para realizar pruebas rápidas y verificar el funcionamiento de la API directamente desde **VS Code** si tienes instalada la extensión **REST Client**.

---

<div align="center">
  <p>Realizado por <strong>[PON TU NOMBRE AQUÍ]</strong></p>
  <p>Curso 2024/2025</p>
</div>

---
## Autor 👨‍💻

Lucilene Vidal Lima