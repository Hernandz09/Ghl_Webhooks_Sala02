<div align="center">

# 🏥 GHL Sala 02 - Sistema de Citas

[![Django](https://img.shields.io/badge/Django-5.2.6-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)

**Sistema de gestión de citas integrado con GoHighLevel (GHL) API**

*Una solución completa para la gestión de citas médicas con integración a GoHighLevel*

</div>

## 📁 Estructura del Proyecto

```
GHL_SALA02/
├── 🐍 backend/                 # Django REST API
│   ├── 📅 appointments/        # App de gestión de citas
│   ├── ⚙️ mi_proyecto/        # Configuración Django
│   ├── 🚀 manage.py
│   └── 📋 requirements.txt
├── ⚛️ frontend/               # React + TypeScript + Vite
│   ├── 📂 src/
│   │   ├── 🔌 api/           # Cliente API
│   │   ├── 🧩 components/    # Componentes React
│   │   └── 📄 pages/         # Páginas de la aplicación
│   ├── 📦 package.json
│   └── ⚡ vite.config.ts
├── 📚 docs/                   # Documentación
├── 🔧 scripts/                # Scripts de utilidad
└── 🐍 venv/                   # Entorno virtual Python
```

## 🛠️ Stack Tecnológico

### 🐍 Backend
<table>
<tr>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg" width="40" height="40"/>
<br><b>Django 5.2.6</b>
<br><small>Framework web</small>
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg" width="40" height="40"/>
<br><b>MySQL</b>
<br><small>Base de datos</small>
</td>
<td align="center" width="25%">
<img src="https://img.icons8.com/color/48/000000/api.png" width="40" height="40"/>
<br><b>Django REST</b>
<br><small>API REST</small>
</td>
<td align="center" width="25%">
<img src="https://img.icons8.com/color/48/000000/medical-doctor.png" width="40" height="40"/>
<br><b>GoHighLevel</b>
<br><small>Integración GHL</small>
</td>
</tr>
</table>

### ⚛️ Frontend
<table>
<tr>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" width="40" height="40"/>
<br><b>React 18</b>
<br><small>Biblioteca de UI</small>
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="40" height="40"/>
<br><b>TypeScript</b>
<br><small>Tipado estático</small>
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vitejs/vitejs-original.svg" width="40" height="40"/>
<br><b>Vite</b>
<br><small>Build tool</small>
</td>
<td align="center" width="25%">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/axios/axios-original.svg" width="40" height="40"/>
<br><b>Axios</b>
<br><small>Cliente HTTP</small>
</td>
</tr>
</table>

## 🚀 Configuración Rápida

### 📋 Prerrequisitos
- [ ] Python 3.8+
- [ ] Node.js 16+
- [ ] MySQL 8.0+
- [ ] Git

### ⚡ Instalación Express

<details>
<summary><b>🔧 Opción 1: Scripts Automatizados</b></summary>

```bash
# 1. Clonar repositorio
git clone <tu-repositorio>
cd GHL_SALA02

# 2. Ejecutar script de instalación
scripts/install-deps.bat

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 4. Iniciar desarrollo
scripts/start-dev.bat
```

</details>

<details>
<summary><b>🛠️ Opción 2: Instalación Manual</b></summary>

#### 1️⃣ **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd GHL_SALA02
```

#### 2️⃣ **Configurar variables de entorno**
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
# ⚠️ IMPORTANTE: El archivo .env NO se sube a Git por seguridad
```

#### 3️⃣ **Configurar la base de datos**
- Crear una base de datos MySQL
- Configurar las credenciales en el archivo `.env`

#### 4️⃣ **Backend**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### 5️⃣ **Frontend**
```bash
cd frontend
npm install
npm run dev
```

</details>

### 🎯 URLs de Desarrollo
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

## 🔐 Variables de Entorno

<div align="center">

**⚠️ IMPORTANTE**: Debes crear un archivo `.env` en la raíz del proyecto

</div>

<details>
<summary><b>🗄️ Base de Datos</b></summary>

```env
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
```

</details>

<details>
<summary><b>🐍 Django</b></summary>

```env
SECRET_KEY=tu-secret-key-super-seguro
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

</details>

<details>
<summary><b>🏥 GoHighLevel API</b></summary>

```env
GHL_ACCESS_TOKEN=tu_token_de_acceso_ghl
GHL_API_KEY=tu_api_key_ghl
```

</details>

<details>
<summary><b>🌐 CORS</b></summary>

```env
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

</details>

> **📝 Nota**: Usa el archivo `.env.example` como plantilla y reemplaza los valores con tus credenciales reales.

## 🔌 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/appointments/` | 📋 Listar todas las citas |
| `POST` | `/api/appointments/` | ➕ Crear nueva cita |
| `PUT` | `/api/appointments/{id}/` | ✏️ Actualizar cita existente |
| `DELETE` | `/api/appointments/{id}/` | 🗑️ Eliminar cita |

## 🎯 Características Principales

- ✅ **Gestión completa de citas** - CRUD completo
- 🔗 **Integración con GoHighLevel** - Sincronización automática
- 🎨 **Interfaz moderna** - React + TypeScript
- 🚀 **API REST robusta** - Django REST Framework
- 📱 **Responsive design** - Adaptable a dispositivos móviles
- 🔒 **Seguridad** - Variables de entorno protegidas

## 📚 Documentación Adicional

<div align="center">

| Documento | Descripción |
|-----------|-------------|
| 📖 **[Guía de Configuración](docs/SETUP.md)** | Configuración paso a paso |
| 🔐 **[Variables de Entorno](docs/ENV_SETUP.md)** | Configuración detallada del archivo .env |
| 🔧 **[Scripts de Utilidad](scripts/)** | Scripts para automatizar tareas |

</div>

## ⚠️ Notas Importantes

<div align="center">

| ⚠️ | **El archivo `.env` NO se incluye en el repositorio** por seguridad |
| 📝 | Debes crear tu propio archivo `.env` basado en `.env.example` |
| 📚 | Revisa la documentación en `docs/` para configuración detallada |

</div>

---

<div align="center">

**🏥 GHL Sala 02 - Sistema de Citas**  
*Desarrollado con ❤️ para la gestión eficiente de citas médicas*

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)

</div>
