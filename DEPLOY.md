# Guía de Despliegue en AWS EC2

## Requisitos Previos
- Una instancia EC2 con Ubuntu 20.04 o 22.04
- Acceso SSH a la instancia
- Python 3.8+ instalado

## Pasos de Despliegue

### 1. Conectar a tu instancia EC2
```bash
ssh -i tu-llave.pem ubuntu@13.222.177.100
```

### 2. Actualizar el sistema
```bash
sudo apt update
sudo apt upgrade -y
```

### 3. Instalar dependencias del sistema
```bash
sudo apt install -y python3-pip python3-venv nginx git
```

### 4. Clonar el repositorio
```bash
cd /home/ubuntu
git clone https://github.com/tu-usuario/Proyecto-Integrador-1-EstudIAntes.git
cd Proyecto-Integrador-1-EstudIAntes
```

### 5. Crear y activar entorno virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 6. Instalar dependencias de Python
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 7. Configurar variables de entorno
```bash
cp .env.example .env
nano .env
```

Edita el archivo `.env` con tus valores:
- Genera un `DJANGO_SECRET_KEY` seguro
- Configura `DJANGO_DEBUG=False`
- Agrega tu `OPENAI_API_KEY`

Para generar un SECRET_KEY:
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 8. Recolectar archivos estáticos
```bash
python manage.py collectstatic --noinput
```

### 9. Aplicar migraciones
```bash
python manage.py migrate
```

### 10. Crear superusuario
```bash
python manage.py createsuperuser
```

### 11. Configurar Gunicorn como servicio systemd
Crear archivo de servicio:
```bash
sudo nano /etc/systemd/system/estudiantes.service
```

Contenido del archivo:
```ini
[Unit]
Description=EstudIAntes Django Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Proyecto-Integrador-1-EstudIAntes
Environment="PATH=/home/ubuntu/Proyecto-Integrador-1-EstudIAntes/.venv/bin"
ExecStart=/home/ubuntu/Proyecto-Integrador-1-EstudIAntes/.venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          schedule.wsgi:application

[Install]
WantedBy=multi-user.target
```

Activar el servicio:
```bash
sudo systemctl daemon-reload
sudo systemctl start estudiantes
sudo systemctl enable estudiantes
sudo systemctl status estudiantes
```

### 12. Configurar Nginx
Crear archivo de configuración:
```bash
sudo nano /etc/nginx/sites-available/estudiantes
```

Contenido del archivo:
```nginx
server {
    listen 80;
    server_name 13.222.177.100;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/ubuntu/Proyecto-Integrador-1-EstudIAntes/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activar el sitio:
```bash
sudo ln -s /etc/nginx/sites-available/estudiantes /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 13. Configurar el firewall (Security Group en AWS)
En la consola de AWS, asegúrate de que el Security Group de tu instancia EC2 permite:
- Puerto 80 (HTTP) desde 0.0.0.0/0
- Puerto 22 (SSH) desde tu IP

### 14. Verificar el despliegue
Abre en tu navegador: `http://13.222.177.100`

## Comandos Útiles

### Ver logs de Gunicorn
```bash
sudo journalctl -u estudiantes -f
```

### Reiniciar servicios después de cambios en código
```bash
cd /home/ubuntu/Proyecto-Integrador-1-EstudIAntes
git pull
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart estudiantes
```

### Ver logs de Nginx
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## Solución de Problemas

### Error 502 Bad Gateway
- Verifica que Gunicorn esté corriendo: `sudo systemctl status estudiantes`
- Revisa logs: `sudo journalctl -u estudiantes -n 50`

### Archivos estáticos no se cargan
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Base de datos bloqueada
```bash
# Asegúrate de que solo Gunicorn accede a la DB
sudo systemctl restart estudiantes
```

## Configuración HTTPS (Opcional con Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

## Actualizaciones
Cuando hagas cambios en el código:
```bash
cd /home/ubuntu/Proyecto-Integrador-1-EstudIAntes
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart estudiantes
```
