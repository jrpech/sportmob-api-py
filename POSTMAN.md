# Colección de Postman para API SportMob Python

Esta es una colección básica para importar en Postman y probar la API.

## Importar en Postman

1. Abre Postman
2. Click en "Import"
3. Arrastra este archivo o pega el contenido JSON de abajo
4. La colección aparecerá en tu workspace

## Colección JSON

```json
{
  "info": {
    "name": "API SportMob Python",
    "description": "API compatible con JWT de .NET",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/health",
          "host": ["{{base_url}}"],
          "path": ["health"]
        }
      }
    },
    {
      "name": "Login",
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "// Guardar token automáticamente",
              "if (pm.response.code === 200) {",
              "    var jsonData = pm.response.json();",
              "    if (jsonData.data && jsonData.data.token) {",
              "        pm.environment.set('jwt_token', jsonData.data.token);",
              "        console.log('Token guardado:', jsonData.data.token.substring(0, 20) + '...');",
              "    }",
              "}"
            ]
          }
        }
      ],
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"usuario\": \"usuario@example.com\",\n  \"contrasena\": \"password123\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/api/Login/auth",
          "host": ["{{base_url}}"],
          "path": ["api", "Login", "auth"]
        }
      }
    },
    {
      "name": "User Perfil (Protected)",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{jwt_token}}",
            "type": "text"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/User/perfil",
          "host": ["{{base_url}}"],
          "path": ["api", "User", "perfil"]
        }
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000",
      "type": "string"
    }
  ]
}
```

## Variables de Entorno

Crea un environment en Postman con estas variables:

- `base_url`: http://localhost:8000
- `jwt_token`: (se llenará automáticamente después del login)

## Uso

1. Ejecuta el request "Login" con credenciales válidas
2. El token se guarda automáticamente en la variable `jwt_token`
3. Los requests protegidos usarán automáticamente este token
