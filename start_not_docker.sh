#!/bin/bash

set -e

echo "Iniciando API SportMob Python sin Docker..."
echo ""

if ! command -v python3 &> /dev/null; then
	echo "Error: python3 no está instalado o no está en el PATH"
	exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
case "$PYTHON_VERSION" in
	3.10|3.11|3.12|3.13)
		;;
	*)
		echo "Error: este proyecto no está listo para Python $PYTHON_VERSION"
		echo "Usa Python 3.10, 3.11, 3.12 o 3.13 para crear el entorno virtual."
		echo "En tu equipo, python3 apunta a una versión incompatible para algunas dependencias como Pillow."
		exit 1
		;;
esac

if [ ! -d venv ]; then
	echo "Creando entorno virtual en ./venv..."
	python3 -m venv venv
fi

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Actualizando pip..."
python -m pip install --upgrade pip

echo "Instalando dependencias..."
pip install -r requirements.txt

if [ ! -f .env ]; then
	echo "Creando archivo .env desde .env.example..."
	cp .env.example .env
	echo ""
	echo "Se creó .env con valores por defecto."
	echo "Para correr sin Docker, revisa DB_HOST y usa tu MySQL local o remoto."
fi

if grep -Eq '^DB_HOST=db$' .env; then
	echo ""
	echo "Aviso: DB_HOST=db en .env normalmente solo funciona con Docker Compose."
	echo "Si vas a correr sin Docker, cambia DB_HOST por localhost o por la IP de tu servidor MySQL."
	echo ""
fi

echo ""
echo "La API se levantará en http://localhost:8000"
echo "Swagger UI: http://localhost:8000/swagger"
echo ""
echo "Presiona Ctrl+C para detenerla."
echo ""

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
