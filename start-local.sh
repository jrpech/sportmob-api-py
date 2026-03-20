#!/bin/bash

# Script para desarrollo local con MySQL incluido

echo "🚀 Iniciando API SportMob Python (Modo Local con MySQL)..."
echo ""

if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    exit 1
fi

if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde .env.example..."
    cp .env.example .env
fi

echo "🛑 Deteniendo contenedores existentes..."
docker-compose -f docker-compose.local.yml down

echo "🏗️  Construyendo imágenes..."
docker-compose -f docker-compose.local.yml build

echo "▶️  Levantando servicios (API + MySQL local)..."
docker-compose -f docker-compose.local.yml up -d

echo ""
echo "✅ Servicios iniciados correctamente!"
echo ""
echo "📊 Accede a:"
echo "   - API: http://localhost:8000"
echo "   - Swagger UI: http://localhost:8000/swagger"
echo "   - MySQL local: localhost:3307"
echo ""
echo "📋 Ver logs: docker-compose -f docker-compose.local.yml logs -f api"
echo "🛑 Detener: docker-compose -f docker-compose.local.yml down"
echo ""

docker-compose -f docker-compose.local.yml logs -f api
