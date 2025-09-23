# Guía de Configuración Inicial

## 🚀 Configuración Rápida

### 1. Clonar el Repositorio
```bash
git clone <tu-repositorio>
cd GHL_SALA02
```

### 2. Configurar Variables de Entorno
**⚠️ PASO OBLIGATORIO**: Debes crear el archivo `.env` antes de continuar.

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar con tus credenciales
# Usa cualquier editor: notepad, vscode, etc.
```

### 3. Instalar Dependencias
```bash
# Opción 1: Script automático (Windows)
scripts/install-deps.bat

# Opción 2: Manual
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

### 4. Configurar Base de Datos
1. Crear una base de datos MySQL
2. Configurar las credenciales en `.env`
3. Ejecutar migraciones:
```bash
cd backend
python manage.py migrate
```

### 5. Iniciar Servidores
```bash
# Opción 1: Script automático (Windows)
scripts/start-dev.bat

# Opción 2: Manual
# Terminal 1 - Backend
cd backend && python manage.py runserver

# Terminal 2 - Frontend  
cd frontend && npm run dev
```

## 🔧 Configuración Detallada

### Variables de Entorno Requeridas

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `DB_NAME` | Nombre de la base de datos | `ghl_sala02_db` |
| `DB_USER` | Usuario de MySQL | `root` |
| `DB_PASSWORD` | Contraseña de MySQL | `tu_password` |
| `DB_HOST` | Host de la base de datos | `localhost` |
| `DB_PORT` | Puerto de MySQL | `3306` |
| `SECRET_KEY` | Clave secreta de Django | `django-insecure-...` |
| `DEBUG` | Modo debug | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos | `127.0.0.1,localhost` |
| `GHL_ACCESS_TOKEN` | Token de GoHighLevel | `ghl_token_...` |
| `GHL_API_KEY` | API Key de GoHighLevel | `ghl_api_...` |

### Estructura del Archivo .env
```env
# Base de Datos
DB_NAME=ghl_sala02_db
DB_USER=root
DB_PASSWORD=tu_password_seguro
DB_HOST=localhost
DB_PORT=3306

# Django
SECRET_KEY=django-insecure-tu-secret-key-muy-largo-y-seguro
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# GoHighLevel
GHL_ACCESS_TOKEN=ghl_token_tu_token_aqui
GHL_API_KEY=ghl_api_tu_api_key_aqui

# CORS
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## 🐛 Solución de Problemas

### Error: "No module named 'django'"
```bash
# Activar el entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r backend/requirements.txt
```

### Error: "Cannot connect to database"
- Verificar que MySQL esté ejecutándose
- Revisar las credenciales en `.env`
- Crear la base de datos si no existe

### Error: "Module not found" en Frontend
```bash
cd frontend
npm install
```

## 📞 Soporte

Si tienes problemas con la configuración:
1. Revisa que todas las variables de entorno estén configuradas
2. Verifica que las dependencias estén instaladas
3. Asegúrate de que MySQL esté ejecutándose
4. Revisa los logs de error en la consola
