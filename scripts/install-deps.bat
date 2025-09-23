@echo off
echo Instalando dependencias del proyecto...

echo.
echo Instalando dependencias del Backend...
cd backend
pip install -r requirements.txt

echo.
echo Instalando dependencias del Frontend...
cd ..\frontend
npm install

echo.
echo Dependencias instaladas correctamente!
echo.
pause
