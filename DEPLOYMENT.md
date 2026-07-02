# Guía de Despliegue - Fuchivola en Vercel + Azure Database

## Requisitos previos
- Cuenta en Vercel (vercel.com)
- Cuenta en Azure (azure.microsoft.com)
- Git configurado

## Paso 1: Preparar Azure Database for PostgreSQL

1. Ir a Azure Portal > Crear un recurso > Base de datos para PostgreSQL
2. Seleccionar "Servidor flexible"
3. Configurar:
   - Nombre: `fuchivola-db`
   - Usuario administrador: `dbadmin`
   - Contraseña: (generar una fuerte)
   - Región: (cerca de tu ubicación)
4. En Networking > Reglas de firewall:
   - Permitir acceso desde Vercel
   - Agregar dirección IP: 0.0.0.0 - 255.255.255.255 (o específica de Vercel)

5. Copiar la cadena de conexión desde el portal Azure

## Paso 2: Configurar Vercel

1. Ir a vercel.com y conectar tu repositorio GitHub
2. En Project Settings > Environment Variables, agregar:
   ```
   SECRET_KEY=tu-clave-secreta-aqui
   DEBUG=False
   ALLOWED_HOSTS=tu-proyecto.vercel.app
   DB_ENGINE=postgresql
   DB_NAME=postgres
   DB_USER=dbadmin
   DB_PASSWORD=tu-contraseña-azure
   DB_HOST=tu-servidor.postgres.database.azure.com
   DB_PORT=5432
   ```

3. En Build & Development Settings:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn fuchivola.wsgi:application`

## Paso 3: Archivo .env local

1. Copiar `.env.example` a `.env`
2. Llenar con tus valores reales:
   ```bash
   cp .env.example .env
   ```

## Paso 4: Instalar dependencias

```bash
pip install -r requirements.txt
```

## Paso 5: Ejecutar migraciones

Antes de desplegar a Vercel, ejecuta localmente:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

## Paso 6: Desplegar a Vercel

```bash
git add .
git commit -m "Configurar Vercel + Azure Database"
git push origin main
```

Vercel detectará los cambios y desplegará automáticamente.

## Paso 7: Ejecutar migraciones en Vercel

Usa la consola de Vercel o accede por SSH para ejecutar:
```bash
python manage.py migrate
python manage.py createsuperuser
```

## Troubleshooting

- Si hay errores de conexión a BD: verifica IP whitelist en Azure
- Si falta STATIC_ROOT: Django lo creará automáticamente
- Para archivos media en Vercel: considera usar Azure Blob Storage

## Archivos generados
- `vercel.json` - Configuración de Vercel
- `.env.example` - Plantilla de variables de entorno
- `requirements.txt` - Dependencias Python actualizadas
- `settings.py` - Actualizado para soportar variables de entorno
