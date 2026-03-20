@echo off
REM Script para iniciar el proyecto con Docker en Windows

echo Iniciando API SportMob Python con Docker...
echo.

REM Verificar que Docker está instalado
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Docker no esta instalado
    echo Instala Docker desde: https://www.docker.com/get-started
    exit /b 1
)

REM Verificar si existe archivo .env
if not exist .env (
    echo Creando archivo .env desde .env.example...
    copy .env.example .env
)

REM Detener contenedores existentes
echo Deteniendo contenedores existentes...
docker-compose down

REM Construir y levantar servicios
echo Construyendo imagenes...
docker-compose build

echo Levantando servicios...
docker-compose up -d

echo.
echo Servicios iniciados correctamente!
echo.
echo Accede a:
echo    - API: http://localhost:8000
echo    - Swagger UI: http://localhost:8000/swagger
echo    - ReDoc: http://localhost:8000/redoc
echo.
echo Ver logs: docker-compose logs -f api
echo Detener: docker-compose down
echo.

REM Mostrar logs
docker-compose logs -f api
