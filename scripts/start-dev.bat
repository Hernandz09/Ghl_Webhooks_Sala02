@echo off
echo Iniciando servidor de desarrollo...

echo.
echo Iniciando Backend (Django)...
start "Backend" cmd /k "cd backend && python manage.py runserver"

echo.
echo Iniciando Frontend (React)...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Servidores iniciados:
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:5173
echo.
pause
