# GHL Sala 02 - Sistema de Citas

Sistema de gestión de citas integrado con GoHighLevel (GHL) API.

## Estructura del Proyecto

```
GHL_SALA02/
├── backend/                 # Django REST API
│   ├── appointments/        # App de gestión de citas
│   ├── mi_proyecto/        # Configuración Django
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # React + TypeScript + Vite
│   ├── src/
│   │   ├── api/           # Cliente API
│   │   ├── components/    # Componentes React
│   │   └── pages/         # Páginas de la aplicación
│   ├── package.json
│   └── vite.config.ts
├── docs/                   # Documentación
├── scripts/                # Scripts de utilidad
└── venv/                   # Entorno virtual Python
```

## Tecnologías

### Backend
- **Django 5.2.6** - Framework web
- **Django REST Framework** - API REST
- **MySQL** - Base de datos
- **GoHighLevel API** - Integración con GHL

### Frontend
- **React 18** - Biblioteca de UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool
- **Axios** - Cliente HTTP

## Configuración

1. **Clonar el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd GHL_SALA02
   ```

2. **Configurar variables de entorno**:
   ```bash
   # Copiar el archivo de ejemplo
   cp .env.example .env
   
   # Editar .env con tus credenciales
   # ⚠️ IMPORTANTE: El archivo .env NO se sube a Git por seguridad
   ```

3. **Configurar la base de datos**:
   - Crear una base de datos MySQL
   - Configurar las credenciales en el archivo `.env`

3. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

4. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Variables de Entorno Requeridas

**⚠️ IMPORTANTE**: Debes crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

### Base de Datos
```env
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
```

### Django
```env
SECRET_KEY=tu-secret-key-super-seguro
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### GoHighLevel API
```env
GHL_ACCESS_TOKEN=tu_token_de_acceso_ghl
GHL_API_KEY=tu_api_key_ghl
```

### CORS
```env
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**📝 Nota**: Usa el archivo `.env.example` como plantilla y reemplaza los valores con tus credenciales reales.

## API Endpoints

- `GET /api/appointments/` - Listar citas
- `POST /api/appointments/` - Crear cita
- `PUT /api/appointments/{id}/` - Actualizar cita
- `DELETE /api/appointments/{id}/` - Eliminar cita

## Desarrollo

El frontend corre en `http://localhost:5173` y el backend en `http://localhost:8000`.

## 📚 Documentación Adicional

- **[Guía de Configuración](docs/SETUP.md)** - Configuración paso a paso
- **[Variables de Entorno](docs/ENV_SETUP.md)** - Configuración detallada del archivo .env
- **[Scripts de Utilidad](scripts/)** - Scripts para automatizar tareas

## ⚠️ Notas Importantes

- **El archivo `.env` NO se incluye en el repositorio** por seguridad
- Debes crear tu propio archivo `.env` basado en `.env.example`
- Revisa la documentación en `docs/` para configuración detallada
