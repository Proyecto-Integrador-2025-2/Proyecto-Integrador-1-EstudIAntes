"""
Django settings for schedule project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from django.contrib.messages import constants as messages

# --- Paths base ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Cargar variables desde .env en la raíz del proyecto ---
# Esto garantiza que se lea aunque ejecutes comandos desde otra carpeta
load_dotenv(BASE_DIR / ".env")

# --- Utilidades ---
def env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")

# --- Seguridad / Debug ---
# Nunca dejes la SECRET_KEY hardcodeada en prod. Para dev, ponemos un fallback.
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "dev-insecure-key-ONLY-FOR-LOCAL",  # fallback seguro sólo para desarrollo local
)

DEBUG = env_bool("DJANGO_DEBUG", True)

# Para desarrollo local
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "testserver",
]

# Si usas túneles o dominios externos en dev, añádelos por env:
extra_hosts = os.getenv("ALLOWED_HOSTS_EXTRA", "")
if extra_hosts:
    ALLOWED_HOSTS += [h.strip() for h in extra_hosts.split(",") if h.strip()]

# --- Apps instaladas ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps del proyecto
    "busyschedule",
    "content",
    "chat",
    "accounts",
    # "django_htmx"
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "django_htmx.middleware.HtmxMiddleware",  # si usas HTMX, descomenta
]

ROOT_URLCONF = "schedule.urls"

# --- Templates ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # templates globales en /templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "schedule.wsgi.application"

# --- Base de datos (sqlite para dev) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Validadores de contraseña ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internacionalización ---
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True  # Mantener True para que Django guarde en UTC y convierta a tu zona

# --- Archivos estáticos ---
STATIC_URL = "static/"
# Si tienes una carpeta /static en la raíz para assets globales:
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
# Para collectstatic en despliegues (no afecta dev si no lo usas):
STATIC_ROOT = BASE_DIR / "staticfiles"

# --- Default PK ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Auth redirects ---
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# --- OpenAI ---
# Se usa en tu app `chat`. No es obligatorio estar en settings,
# pero lo dejamos aquí por conveniencia.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
