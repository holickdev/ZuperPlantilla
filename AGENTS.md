# AGENTS.md — Guía y Reglas del Proyecto

Este documento establece la arquitectura, las convenciones de código y las reglas que **todos los agentes de IA y desarrolladores** deben seguir al trabajar o modificar este repositorio.

---

## 📌 1. Propósito del Proyecto y Audiencia

Este repositorio es una **plantilla educativa** diseñada para estudiantes de Python que están aprendiendo:
- Arquitectura Servidor-Cliente (Server-Side Rendering con Flask y Jinja2).
- Conexión a bases de datos relacionales (MySQL).
- Principios de código limpio y separación básica de responsabilidades.

Al ser un proyecto de nivel inicial e intermedio, **se debe priorizar la claridad, el orden y las buenas prácticas sencillas**, evitando sobre-diseñar o agregar abstracciones complejas e innecesarias (principio YAGNI).

---

## 🌐 2. Reglas de Idioma y Estilo (Crítico)

| Elemento | Idioma Obligatorio | Ejemplo |
|---|---|---|
| **Código Fuente** (Variables, funciones, módulos, rutas, BD) | **Inglés** | `verify_credentials`, `register_user`, `user_service.py`, `main_bp`, `email` |
| **Comentarios en Código** | **Español** | `# Verifica la contraseña con bcrypt` |
| **Interfaz de Usuario (UI HTML / Mensajes Flash)** | **Español** | `"Credenciales incorrectas"`, `<h2>Bienvenido</h2>` |

---

## 🏗️ 3. Arquitectura del Proyecto

El proyecto sigue una arquitectura **App Factory + Blueprint Único (`main_bp`)** estructurada en 3 capas simples:

```text
Desacoplado/
├── AGENTS.md                   # Instrucciones y reglas del proyecto
├── .env                        # Variables de entorno (DB_HOST, SECRET_KEY, etc.)
├── requirements.txt            # Dependencias instaladas
├── run.py                      # Punto de entrada de la aplicación
└── app/
    ├── __init__.py              # App Factory (crea Flask app y registra main_bp)
    ├── database.py              # Proveedor de conexión a MySQL (get_db_connection)
    ├── routes/
    │   └── main.py              # Rutas HTTP, sesión y decorador @login_required
    ├── services/
    │   └── user_service.py      # Lógica de datos, SQL y criptografía bcrypt
    ├── static/                  # Estilos CSS estáticos
    └── templates/               # Plantillas HTML planas (index, login, sign-up, dashboard)
```

---

## 🛡️ 4. Reglas de Desarrollo y Buenas Prácticas

### 4.1. Separación de Responsabilidades (SRP)
- **Rutas (`app/routes/main.py`):** Su ÚNICA función es recibir solicitudes HTTP, procesar formularios, gestionar sesiones (`session`), invocar la capa de servicios y renderizar plantillas o redirigir. **Nunca** deben contener consultas SQL directas ni hashing de contraseñas.
- **Servicios (`app/services/user_service.py`):** Su ÚNICA función es comunicarse con la base de datos MySQL y aplicar la lógica de hashing (`bcrypt`). **Nunca** deben importar `flask`, `request` ni manejar sesiones HTTP.
- **Conexión a BD (`app/database.py`):** Proporciona la función `get_db_connection()`.

### 4.2. Manejo Seguro de Recursos y Datos
- **Cierre de Conexiones:** Toda función en la capa de servicios que abra un cursor o conexión a MySQL **debe hacer `close()` dentro de un bloque `finally`**.
- **Sanitización de Datos:** Eliminar el campo `'password'` de cualquier diccionario devuelto por la capa de servicios antes de enviarlo a la capa de rutas.
- **Manejo de Excepciones:** Capturar explícitamente excepciones de base de datos como `mysql.connector.IntegrityError` (para correos duplicados) y retornar valores booleanos (`True`/`False`) o limpios a la capa de rutas.

### 4.3. Plantillas HTML
- Las vistas en `app/templates/` deben ser **minimalistas y planas**, utilizando `url_for()` dinámico de Jinja2 para las acciones de formularios y enlaces.
- Deben incluir la estructura para capturar y mostrar mensajes `flash` enviados desde Flask.

---

## ⚡ 5. Comandos de Ejecución

1. **Activar entorno virtual:**
   ```powershell
   .\venv\Scripts\activate
   ```
2. **Ejecutar servidor:**
   ```powershell
   python run.py
   ```
