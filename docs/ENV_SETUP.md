# 🔐 Configuración de Variables de Entorno

## ⚠️ IMPORTANTE: Debes crear el archivo .env

**El archivo `.env` NO se incluye en el repositorio por seguridad.**

### Pasos para configurar:

1. **Copia el archivo de ejemplo:**
   ```bash
   cp .env.example .env
   ```

2. **Edita el archivo `.env` con tus credenciales:**
   ```bash
   # Usa cualquier editor
   notepad .env
   # o
   code .env
   ```

3. **Reemplaza los valores de ejemplo con tus datos reales:**

### Variables Requeridas:

#### 🗄️ Base de Datos MySQL
```env
DB_NAME=ghl_sala02_db          # Nombre de tu base de datos
DB_USER=root                   # Usuario de MySQL
DB_PASSWORD=tu_password        # Contraseña de MySQL
DB_HOST=localhost              # Host de la base de datos
DB_PORT=3306                   # Puerto de MySQL
```

#### 🐍 Django
```env
SECRET_KEY=django-insecure-tu-secret-key-muy-largo-y-seguro
DEBUG=True                     # False en producción
ALLOWED_HOSTS=127.0.0.1,localhost
```

#### 🔗 GoHighLevel API
```env
GHL_ACCESS_TOKEN=ghl_token_tu_token_aqui
GHL_API_KEY=ghl_api_tu_api_key_aqui
```

#### 🌐 CORS
```env
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Ejemplo de archivo .env completo:
```env
# Base de Datos
DB_NAME=ghl_sala02_db
DB_USER=root
DB_PASSWORD=mi_password_seguro
DB_HOST=localhost
DB_PORT=3306

# Django
SECRET_KEY=django-insecure-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# GoHighLevel
GHL_ACCESS_TOKEN=ghl_token_abc123def456
GHL_API_KEY=ghl_api_xyz789uvw456

# CORS
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### 🚨 Seguridad:
- **NUNCA** subas el archivo `.env` a Git
- **NUNCA** compartas tus credenciales
- Usa contraseñas seguras
- En producción, usa `DEBUG=False`

### ✅ Verificación:
Después de crear el archivo `.env`, puedes verificar que funciona ejecutando:
```bash
cd backend
python manage.py check
```

Si no hay errores, la configuración es correcta.
