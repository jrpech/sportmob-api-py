#!/bin/bash

# =============================================================================
# Ejemplos de peticiones cURL para probar la API
# =============================================================================

API_URL="http://localhost:8000"

echo "======================================"
echo "Ejemplos de cURL para API SportMob"
echo "======================================"
echo ""

# =============================================================================
# 1. HEALTH CHECK
# =============================================================================
echo "1️⃣  Health Check"
echo "--------------------------------------"
echo "curl -X GET $API_URL/health"
echo ""
curl -X GET "$API_URL/health"
echo -e "\n\n"

# =============================================================================
# 2. LOGIN
# =============================================================================
echo "2️⃣  Login (obtener token)"
echo "--------------------------------------"
echo 'curl -X POST $API_URL/api/Login/auth \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{"usuario": "usuario@example.com", "contrasena": "password123"}'"'"
echo ""

# Ejecutar login y guardar respuesta
RESPONSE=$(curl -s -X POST "$API_URL/api/Login/auth" \
  -H "Content-Type: application/json" \
  -d '{"usuario": "usuario@example.com", "contrasena": "password123"}')

echo "$RESPONSE"
echo ""

# Extraer token de la respuesta (requiere jq)
if command -v jq &> /dev/null; then
    TOKEN=$(echo "$RESPONSE" | jq -r '.data.token // empty')
    
    if [ ! -z "$TOKEN" ]; then
        echo "✅ Token obtenido:"
        echo "$TOKEN"
        echo ""
        
        # =============================================================================
        # 3. ENDPOINT PROTEGIDO (ejemplo)
        # =============================================================================
        echo -e "\n3️⃣  Endpoint protegido (requiere token)"
        echo "--------------------------------------"
        echo 'curl -X GET $API_URL/api/User/perfil \'
        echo '  -H "Authorization: Bearer <TOKEN>"'
        echo ""
        
        # Descomentar si implementaste el router de ejemplo
        # curl -X GET "$API_URL/api/User/perfil" \
        #   -H "Authorization: Bearer $TOKEN"
        # echo -e "\n"
    else
        echo "⚠️  No se pudo extrair el token (credenciales incorrectas o BD no disponible)"
    fi
else
    echo "💡 Instala 'jq' para extraer automáticamente el token:"
    echo "   macOS: brew install jq"
    echo "   Ubuntu: sudo apt-get install jq"
fi

echo ""
echo "======================================"
echo "Fin de ejemplos"
echo "======================================"
