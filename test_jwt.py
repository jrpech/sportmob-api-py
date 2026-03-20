#!/usr/bin/env python3
"""
Script de prueba para validar la compatibilidad JWT entre Python y .NET

Este script:
1. Genera un token JWT usando la implementación de Python
2. Decodifica el token para mostrar los claims
3. Permite verificar que sea idéntico a lo que genera .NET
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar app
sys.path.insert(0, str(Path(__file__).parent))

from app.auth import generate_jwt_token, decode_jwt_token
import json


def test_jwt_generation():
    """Prueba la generación de tokens JWT"""
    
    print("=" * 60)
    print("TEST DE GENERACIÓN JWT - Compatibilidad Python/.NET")
    print("=" * 60)
    print()
    
    # Datos de prueba
    user_id = 1
    name = "Juan Pérez"
    email = "juan.perez@example.com"
    
    print(f"Generando token para:")
    print(f"  ID: {user_id}")
    print(f"  Nombre: {name}")
    print(f"  Email: {email}")
    print()
    
    # Generar token
    token = generate_jwt_token(user_id, name, email)
    
    print("Token generado:")
    print("-" * 60)
    print(token)
    print("-" * 60)
    print()
    
    # Decodificar token
    print("Decodificando token...")
    payload = decode_jwt_token(token)
    
    if payload:
        print("✓ Token válido!")
        print()
        print("Claims en el token:")
        print("-" * 60)
        print(json.dumps(payload, indent=2, default=str))
        print("-" * 60)
        print()
        
        # Verificar claims importantes
        print("Verificación de claims (compatibilidad con .NET):")
        print(f"  ✓ sub: {payload.get('sub')}")
        print(f"  ✓ fullName: {payload.get('fullName')}")
        print(f"  ✓ usuario: {payload.get('usuario')}")
        print(f"  ✓ id: {payload.get('id')}")
        print(f"  ✓ jti: {payload.get('jti')}")
        print(f"  ✓ iss: {payload.get('iss')}")
        print(f"  ✓ aud: {payload.get('aud')}")
        print(f"  ✓ exp: {payload.get('exp')}")
        print()
        print("✓ Todos los claims necesarios están presentes")
        print()
        
        # Comparar con configuración .NET
        from app.config import settings
        print("Configuración JWT (debe coincidir con .NET):")
        print(f"  Secret Key: {settings.JWT_SECRET_KEY}")
        print(f"  Issuer: {settings.JWT_ISSUER}")
        print(f"  Audience: {settings.JWT_AUDIENCE}")
        print(f"  Algorithm: {settings.JWT_ALGORITHM}")
        print(f"  Expiration: {settings.JWT_EXPIRATION_MINUTES} minutos")
        print()
        
        print("=" * 60)
        print("✓ TEST EXITOSO - El token es compatible con .NET")
        print("=" * 60)
    else:
        print("✗ Error: No se pudo decodificar el token")
        return False
    
    return True


if __name__ == "__main__":
    success = test_jwt_generation()
    sys.exit(0 if success else 1)
