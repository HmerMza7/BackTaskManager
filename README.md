# TaskManager - Backend

API REST para el sistema de gestión de tareas TaskManager.
Desarrollada como prueba técnica para la Auxiliar 2 UND Desarrollo - CUC.

Repositorio del frontend: https://github.com/HmerMza7/FrontTaskManager

---

## Tecnologías utilizadas

| Tecnología                  | Justificación                                                                                                                                                               |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FastAPI**                 | Framework moderno y de alto rendimiento para APIs REST en Python. Incluye validación automática con Pydantic y documentación Swagger integrada sin configuración adicional. |
| **SQLAlchemy**              | ORM maduro con soporte completo para MySQL. Permite definir modelos como clases Python y mantiene el código desacoplado del motor de base de datos.                         |
| **MySQL**                   | Motor de base de datos relacional robusto, ampliamente utilizado en entornos empresariales.                                                                                 |
| **PyJWT + passlib[bcrypt]** | JWT para autenticación stateless. bcrypt para hash seguro de contraseñas, resistente a ataques de fuerza bruta.                                                             |
| **python-dotenv**           | Manejo de variables de entorno sin exponer credenciales en el repositorio.                                                                                                  |

---

## Requisitos previos

- Python 3.10+
- MySQL 8+
- pip o cualquier gestor de paquetes de Python

---

## Cómo correr el proyecto localmente

### 1. Clonar el repositorio

```bash
git clone https://github.com/HmerMza7/BackTaskManager
cd BackTaskManager
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
o
py -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

crear `.env` con las credenciales de MySQL:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=taskmanager
DB_USER=root
DB_PASSWORD=your_password_here
SECRET_KEY=change_this_to_a_strong_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Crear la base de datos y cargar el esquema

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS taskmanager;"
mysql -u root -p taskmanager < schema.sql
```

En caso de utilizar una interfaz grafica,
ejecutar los siguientes comandos en el editor SQL

CREATE DATABASE IF NOT EXISTS taskmanager;

despues ejecutar el contenido del archivo schema.sql

### 6. Correr el servidor

```bash
uvicorn main:app --reload
```

La API quedará disponible en `http://127.0.0.1:8000`.
Documentación Swagger en `http://127.0.0.1:8000/docs`.

---

## Endpoints

### Autenticación

| Método | Ruta             | Descripción                 |
| ------ | ---------------- | --------------------------- |
| `POST` | `/auth/register` | Registrar nuevo usuario     |
| `POST` | `/auth/login`    | Iniciar sesión, retorna JWT |

### Tareas (requieren Bearer token)

| Método   | Ruta                | Descripción                            |
| -------- | ------------------- | -------------------------------------- |
| `GET`    | `/tasks/`           | Listar tareas con filtros y paginación |
| `POST`   | `/tasks/`           | Crear tarea                            |
| `PUT`    | `/tasks/{id}`       | Actualizar tarea                       |
| `DELETE` | `/tasks/{id}`       | Eliminar tarea                         |
| `GET`    | `/tasks/priorities` | Listar prioridades disponibles         |
| `GET`    | `/tasks/states`     | Listar estados disponibles             |

#### Query params disponibles en GET /tasks/

| Param         | Tipo | Descripción                                     |
| ------------- | ---- | ----------------------------------------------- |
| `page`        | int  | Número de página (default: 1)                   |
| `limit`       | int  | Resultados por página, máximo 100 (default: 10) |
| `state_id`    | int  | Filtrar por estado (1=pendiente, 2=completada)  |
| `priority_id` | int  | Filtrar por prioridad (1=alta, 2=media, 3=baja) |

---

## Estructura del proyecto

```
BackTaskManager/
├── config/
│   └── database.py             # Conexión y sesión de SQLAlchemy
├── controllers/
│   ├── task_controller.py      # Lógica de negocio de tareas
│   └── user_controller.py      # Lógica de registro y login
├── dependencies/
│   └── auth.py                 # Middleware de validación JWT
├── models/
│   ├── task_model.py           # Modelos Task, Priority, StateTask
│   └── user_model.py           # Modelo User
├── routes/
│   ├── auth_routes.py          # Rutas de autenticación y schemas Pydantic
│   └── task_routes.py          # Rutas de tareas y schemas Pydantic
├── services/
│   └── auth_service.py         # Hash de contraseñas y generación de JWT
├── main.py                     # Entrada de la aplicación y CORS
├── schema.sql                  # Estructura e inserción de datos iniciales
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Decisiones técnicas

- **Arquitectura en capas** (routes → controllers → services/models): separa responsabilidades y facilita el mantenimiento. Las rutas solo reciben y validan datos, los controllers contienen la lógica de negocio.
- **Tablas catálogo** (`priority`, `state_task`): en lugar de strings sueltos o ENUMs, se normalizó en tablas separadas. Agregar un nuevo estado o prioridad es un INSERT, no un cambio de schema.
- **JWT stateless**: el `user_id` se extrae directamente del token en cada request, sin consultas adicionales a la base de datos para validar sesión.
- **Ownership validation**: en update y delete se verifica que la tarea pertenezca al usuario autenticado antes de operar, retornando 403 si no corresponde.
- **Filtros y paginación server-side**: los filtros se aplican en la query de base de datos antes del COUNT y del OFFSET/LIMIT, garantizando que el total siempre refleje el resultado filtrado y no el total general.
- **Variables de entorno**: ninguna credencial está hardcodeada en el código.

---
