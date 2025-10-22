# Guía de organización del proyecto — EstudIAntes

Esta guía describe la estructura del repositorio, el propósito de cada carpeta y archivo clave, y cómo ejecutar el proyecto en Windows PowerShell.

## Resumen
EstudIAntes es una aplicación web hecha con Django para gestionar horarios, bloques de disponibilidad y contenido (historias y desafíos). El proyecto está dividido en una configuración global (`schedule`) y varias apps: `busyschedule`, `content` y `chat`.

---

## Estructura principal

Raíz del proyecto:

- `manage.py` — Script de administración de Django. Punto de entrada para ejecutar comandos (`migrate`, `runserver`, `createsuperuser`, etc.).
- `db.sqlite3` — Base de datos SQLite para desarrollo.
- `openAI.env` — Archivo presumiblemente con variables de entorno para OpenAI (no commitear claves sensibles en repositorio público).
- `README.md` — Documentación principal con instrucciones básicas.
- `requirements.txt` — Dependencias del proyecto (ej.: `django`, `django-htmx`, `python-dotenv`, `openai`, `numpy`, `requests`).
- `docs/` — Documentación del proyecto (este archivo se creó aquí).

Carpetas principales:

- `schedule/` — Configuración global del proyecto Django (settings, urls, wsgi/asgi).
- `busyschedule/` — App principal: modelos y vistas para gestionar horarios y bloques de disponibilidad.
- `content/` — App para historias y desafíos (CMS ligero): modelos, fixtures y plantillas.
- `chat/` — App preparada para funcionalidades de chat/IA (actualmente con modelos vacíos o en desarrollo).
- `templates/` — Plantillas globales (layout base y partials compartidos).

---

## Detalle por carpeta y archivos clave

### `schedule/` (configuración del proyecto)
- `settings.py`
  - Carga variables de entorno con `dotenv` (`OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")`).
  - `INSTALLED_APPS` incluye `busyschedule`, `content`, `chat` además de apps contrib de Django.
  - Templates: busca en `BASE_DIR / 'templates'` y en `templates/` de las apps.
  - Base de datos: SQLite (`db.sqlite3`).
  - Nota de seguridad: `SECRET_KEY` está en claro y `DEBUG=True`. Cambiar para producción.
- `urls.py` — Ruteo global (enlaza las URLs de las apps y del admin).
- `wsgi.py`, `asgi.py` — Entrypoints para despliegue.

### `busyschedule/` (gestión de horarios)
- `models.py`
  - `ClassSchedule`: día, `start_time`, `end_time`, `subject`. Método `day_index()` para ordenar días.
  - `AvailableBlock`: día, `start_time`, `end_time`. También tiene `day_index()`.
  - Constantes: `DAYS` y `DAY_ORDER` (días en español y su orden).
- `forms.py`
  - `ClassScheduleForm` y `AvailableBlockForm` para validar y renderizar formularios en templates.
- `views.py`
  - `main_home` — portada simple.
  - `schedule_home` — vista principal para listar horarios y bloques, y para crear nuevos registros.
    - Al crear un horario, elimina bloques disponibles que solapen.
    - Al crear un bloque, unifica bloques solapados (función `merge_available_blocks`).
  - `edit_schedule_modal` — retorna formulario como HTML en JSON para editar desde un modal, y al guardar borra bloques solapados.
  - `delete_schedule`, `delete_block` — confirmación y borrado.
  - `routine_view` — genera una vista tipo rutina (tabla por horas y días) calculando `rowspan` en bloques.
- `templates/` dentro de la app:
  - `home.html` — interfaz principal para añadir y listar horarios y bloques.
  - `edit_form.html`, `delete_modal.html`, `routine.html`, etc.

### `content/` (contenido editorial)
- `models.py`
  - `TimeStamped` (abstracto con `created_at` y `updated_at`).
  - `Tag` — etiquetas.
  - `Challenge` — título, slug (autogenera si falta), summary, body, is_published, tags.
  - `Story` — similar a `Challenge` (teaser + body).
- `fixtures/content_seed.json` — datos de ejemplo que se pueden cargar con `python manage.py loaddata`.
- `templates/content/` — plantillas para listados y detalle (`challenges_list.html`, `challenge_detail.html`, `stories_list.html`).

### `chat/` (chat/IA)
- `models.py` — actualmente vacío (sitio reservado para datos de chat o mensajes).
- `views.py`, `admin.py`, `tests.py` — archivos presentes; podrían contener lógicas de integración con la API de OpenAI.

### `templates/` (global)
- `base.html` — plantilla base utilizada por las apps.
- `partials/pagination.html` — fragmento usado por paginación en listados.

### `migrations/` en cada app
- Contienen los archivos de migración (`0001_initial.py`, etc.) necesarios para crear las tablas en la BD.

---

## Cómo ejecutar el proyecto (Windows PowerShell)

A continuación los pasos recomendados para ejecutar el proyecto en desarrollo en Windows PowerShell.

1) Crear y activar un entorno virtual:

```powershell
python -m venv .venv
# Activar en PowerShell
.venv\Scripts\Activate.ps1
# Si la política de ejecución bloquea scripts, ejecutar (una vez, en PowerShell como administrador):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

2) Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3) Establecer variables de entorno (ejemplo con OpenAI API Key):

- Opción temporal en la sesión PowerShell:

```powershell
$env:OPENAI_API_KEY = "tu_api_key_aqui"
```

- Opción con archivo `.env` (preferido): crea un archivo `.env` en la raíz con:

```
OPENAI_API_KEY=tu_api_key_aqui
```

El `settings.py` ya carga `.env` mediante `dotenv`.

4) Migraciones y datos de ejemplo:

```powershell
python manage.py migrate
python manage.py loaddata content/fixtures/content_seed.json   # opcional
python manage.py createsuperuser   # opcional
```

5) Ejecutar servidor de desarrollo:

```powershell
python manage.py runserver
```

Abrir en el navegador: `http://127.0.0.1:8000/`

---

## Buenas prácticas y notas de seguridad

- No dejar `SECRET_KEY` en `settings.py` en repositorio público. Moverlo a variables de entorno.
- Cambiar `DEBUG=False` en producción y ajustar `ALLOWED_HOSTS`.
- No subir `openAI.env` ni archivos con claves. Usar vaults o variables de entorno del entorno de despliegue.
- Para producción, usar Postgres u otra BD robusta y configurar almacenamiento de archivos/estáticos.

---

## Siguientes pasos recomendados

- Añadir `.env.example` con las variables esperadas.
- Añadir instrucciones de despliegue (e.g., Dockerfile, Gunicorn + Nginx o ASGI + Uvicorn) si se planea desplegar.
- Añadir tests automatizados para la lógica de manejo de bloques/solapamientos.

---

Si quieres, puedo:
- Añadir este documento al `README.md` o crear `docs/ARCHITECTURE.md` en el repo (ya creado).
- Crear un `.env.example` automáticamente.
- Ejecutar `python manage.py check` y `migrate` aquí y reportar resultados.

Dime qué prefieres que haga a continuación.
