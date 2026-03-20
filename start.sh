#!/bin/bash

# Script para iniciar el proyecto con Docker

echo "🚀 Iniciando API SportMob Python con Docker..."
echo ""

# Verificar que Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    echo "   Instala Docker desde: https://www.docker.com/get-started"
    exit 1
fi

# Verificar que Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose no está instalado"
    exit 1
fi

# Verificar si existe archivo .env
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde .env.example..."
    cp .env.example .env
fi

# Detener contenedores existentes
echo "🛑 Deteniendo contenedores existentes..."
docker-compose down

# Construir y levantar servicios
echo "🏗️  Construyendo imágenes..."
docker-compose build

echo "▶️  Levantando servicios..."
docker-compose up -d

echo ""
echo "✅ Servicios iniciados correctamente!"
echo ""
echo "📊 Accede a:"
echo "   - API: http://localhost:8000"
echo "   - Swagger UI: http://localhost:8000/swagger"
echo "   - ReDoc: http://localhost:8000/redoc"
echo ""
echo "📋 Ver logs: docker-compose logs -f api"
echo "🛑 Detener: docker-compose down"
echo ""

# Mostrar logs
docker-compose logs -f api
