# 🎬 Guía de Uso - Sistema de Historias

Guía completa para usar el sistema de historias (stories) en la API SportMob.

## 📋 Tabla de Contenidos

1. [Setup Inicial](#setup-inicial)
2. [Crear una Historia](#crear-una-historia)
3. [Ver Feed de Historias](#ver-feed-de-historias)
4. [Ver Mis Historias](#ver-mis-historias)
5. [Marcar como Vista](#marcar-como-vista)
6. [Eliminar Historia](#eliminar-historia)
7. [Ejemplos con cURL](#ejemplos-con-curl)
8. [Integración con la App](#integración-con-la-app)

---

## Setup Inicial

### 1. Crear las Tablas en la Base de Datos

```bash
# Conectar a la BD y ejecutar el script
mysql -h 146.190.144.229 -P 3306 -u remote-user -pSp0rtm0b2024 sportmob_v2 < database/historias_schema.sql
```

### 2. Levantar la API

```bash
# Con Docker
./start.sh

# Sin Docker
uvicorn main:app --reload
```

### 3. Verificar que funciona

```bash
curl http://localhost:8000/health
```

---

## Crear una Historia

### Endpoint: `POST /api/Historia/crear`

**Headers:**
```
Authorization: Bearer <tu_token_jwt>
Content-Type: multipart/form-data
```

**Body (Form Data):**
- `archivo` (file, requerido): Imagen o video
- `descripcion` (string, opcional): Texto de hasta 500 caracteres
- `duracion_segundos` (int, opcional): 1-15 segundos (default: 5)
- `destacada` (bool, opcional): true para que no expire (default: false)

### Ejemplo con cURL:

```bash
# Historia normal (expira en 24h)
curl -X POST http://localhost:8000/api/Historia/crear \
  -H "Authorization: Bearer TU_TOKEN_JWT" \
  -F "archivo=@/ruta/a/tu/imagen.jpg" \
  -F "descripcion=Mi primera historia!" \
  -F "duracion_segundos=5" \
  -F "destacada=false"

# Historia destacada (no expira)
curl -X POST http://localhost:8000/api/Historia/crear \
  -H "Authorization: Bearer TU_TOKEN_JWT" \
  -F "archivo=@/ruta/a/tu/foto_destacada.jpg" \
  -F "descripcion=Foto del equipo campeón 🏆" \
  -F "duracion_segundos=10" \
  -F "destacada=true"
```

### Response Exitoso:

```json
{
  "respuesta": "OK",
  "mensaje": "Historia creada exitosamente",
  "data": {
    "id": 123,
    "tipo": "imagen",
    "url_archivo": "http://localhost:8000/uploads/historias/2026/03/20/historia_20260320_123456_abc12345.jpg",
    "url_miniatura": "http://localhost:8000/uploads/historias/miniaturas/2026/03/20/thumb_historia_20260320_123456_abc12345.jpg",
    "descripcion": "Mi primera historia!",
    "duracion_segundos": 5,
    "fecha_creacion": "2026-03-20T10:30:00",
    "fecha_expiracion": "2026-03-21T10:30:00",
    "destacada": false,
    "vistas_totales": 0
  }
}
```

### Formatos Soportados:

**Imágenes:**
- JPG/JPEG
- PNG
- GIF
- WEBP

**Videos:**
- MP4
- MOV
- AVI
- WEBM

**Límites:**
- Tamaño máximo: 50 MB
- Duración de video: 30 segundos

---

## Ver Feed de Historias

### Endpoint: `GET /api/Historia/feed`

Obtiene las historias de todos los usuarios, agrupadas por usuario, ordenadas por más recientes.

**Headers:**
```
Authorization: Bearer <tu_token_jwt>
```

**Query Params:**
- `limite` (int, opcional): Número de usuarios (default: 50)

### Ejemplo:

```bash
curl -X GET "http://localhost:8000/api/Historia/feed?limite=20" \
  -H "Authorization: Bearer TU_TOKEN_JWT"
```

### Response:

```json
{
  "respuesta": "OK",
  "mensaje": "",
  "data": {
    "usuarios": [
      {
        "usuario_id": 5,
        "nombre": "Juan",
        "apellido": "Pérez",
        "foto_perfil": "http://...",
        "tiene_historias_nuevas": true,
        "historias": [
          {
            "id": 123,
            "usuario_id": 5,
            "tipo": "imagen",
            "url_archivo": "http://...",
            "url_miniatura": "http://...",
            "descripcion": "Entrenamiento de hoy!",
            "duracion_segundos": 5,
            "ancho": 1080,
            "alto": 1920,
            "fecha_creacion": "2026-03-20T10:30:00",
            "fecha_expiracion": "2026-03-21T10:30:00",
            "activa": true,
            "destacada": false,
            "vistas_totales": 45,
            "visto": false
          }
        ]
      }
    ],
    "total_usuarios": 10,
    "total_historias": 25
  }
}
```

**Nota:** 
- `visto: true` indica que ya viste esa historia
- `tiene_historias_nuevas: true` indica que el usuario tiene historias sin ver
- Las historias destacadas aparecen primero

---

## Ver Mis Historias

### Endpoint: `GET /api/Historia/mis-historias`

Obtiene las historias del usuario autenticado con estadísticas de quién las vio.

**Headers:**
```
Authorization: Bearer <tu_token_jwt>
```

### Ejemplo:

```bash
curl -X GET http://localhost:8000/api/Historia/mis-historias \
  -H "Authorization: Bearer TU_TOKEN_JWT"
```

### Response:

```json
{
  "respuesta": "OK",
  "mensaje": "",
  "data": [
    {
      "id": 123,
      "tipo": "imagen",
      "url_archivo": "http://...",
      "url_miniatura": "http://...",
      "descripcion": "Mi historia",
      "fecha_creacion": "2026-03-20T10:30:00",
      "fecha_expiracion": "2026-03-21T10:30:00",
      "activa": true,
      "destacada": false,
      "vistas_totales": 45,
      "duracion_segundos": 5,
      "visualizadores": [
        {
          "usuario_id": 10,
          "nombre_usuario": "María López",
          "foto_usuario": "http://...",
          "fecha_vista": "2026-03-20T11:00:00",
          "completo": true
        },
        {
          "usuario_id": 15,
          "nombre_usuario": "Carlos García",
          "foto_usuario": "http://...",
          "fecha_vista": "2026-03-20T11:05:00",
          "completo": true
        }
      ]
    }
  ]
}
```

---

## Marcar como Vista

### Endpoint: `POST /api/Historia/{historia_id}/ver`

Registra que viste una historia.

**Headers:**
```
Authorization: Bearer <tu_token_jwt>
Content-Type: application/json
```

**Body:**
```json
{
  "tiempo_visto_segundos": 5,
  "completo": true
}
```

### Ejemplo:

```bash
curl -X POST http://localhost:8000/api/Historia/123/ver \
  -H "Authorization: Bearer TU_TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "tiempo_visto_segundos": 5,
    "completo": true
  }'
```

### Response:

```json
{
  "respuesta": "OK",
  "mensaje": "Vista registrada",
  "data": {
    "historia_id": 123,
    "visto": true,
    "fecha_vista": "2026-03-20T12:00:00"
  }
}
```

---

## Eliminar Historia

### Endpoint: `DELETE /api/Historia/{historia_id}`

Elimina una historia (solo el dueño puede hacerlo).

**Headers:**
```
Authorization: Bearer <tu_token_jwt>
```

### Ejemplo:

```bash
curl -X DELETE http://localhost:8000/api/Historia/123 \
  -H "Authorization: Bearer TU_TOKEN_JWT"
```

### Response:

```json
{
  "respuesta": "OK",
  "mensaje": "Historia eliminada exitosamente",
  "data": null
}
```

---

## Ejemplos con cURL

### Script Completo de Prueba

```bash
#!/bin/bash

# Configuración
API_URL="http://localhost:8000"
TOKEN="TU_TOKEN_JWT"

# 1. Login para obtener token
echo "1. Login..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/api/Login/auth" \
  -H "Content-Type: application/json" \
  -d '{
    "usuario": "usuario@example.com",
    "contrasena": "password123"
  }')

# Extraer token (requiere jq)
TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.data.token')
echo "Token obtenido: ${TOKEN:0:20}..."

# 2. Crear historia
echo -e "\n2. Creando historia..."
curl -X POST "$API_URL/api/Historia/crear" \
  -H "Authorization: Bearer $TOKEN" \
  -F "archivo=@test_image.jpg" \
  -F "descripcion=Historia de prueba desde cURL" \
  -F "duracion_segundos=5" \
  -F "destacada=false"

# 3. Ver feed
echo -e "\n\n3. Obteniendo feed..."
curl -X GET "$API_URL/api/Historia/feed?limite=10" \
  -H "Authorization: Bearer $TOKEN"

# 4. Ver mis historias
echo -e "\n\n4. Obteniendo mis historias..."
curl -X GET "$API_URL/api/Historia/mis-historias" \
  -H "Authorization: Bearer $TOKEN"

# 5. Marcar como vista (cambia 123 por un ID real)
echo -e "\n\n5. Marcando historia 123 como vista..."
curl -X POST "$API_URL/api/Historia/123/ver" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tiempo_visto_segundos": 5, "completo": true}'
```

---

## Integración con la App

### Flujo Recomendado

#### 1. Cargar Feed al Abrir la App

```javascript
// Pseudo-código
async function cargarFeed() {
  const response = await fetch(`${API_URL}/api/Historia/feed?limite=50`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const data = await response.json();
  
  // Mostrar usuarios con historias
  // Destacar los que tienen historias nuevas (tiene_historias_nuevas: true)
  mostrarFeedHistorias(data.data);
}
```

#### 2. Ver Historias de un Usuario

```javascript
async function verHistorias(usuario) {
  // Mostrar historias una por una
  for (const historia of usuario.historias) {
    await mostrarHistoria(historia);
    
    // Marcar como vista
    if (!historia.visto) {
      await marcarComoVista(historia.id, historia.duracion_segundos);
    }
    
    // Esperar antes de la siguiente
    await sleep(historia.duracion_segundos * 1000);
  }
}

async function marcarComoVista(historiaId, duracion) {
  await fetch(`${API_URL}/api/Historia/${historiaId}/ver`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      tiempo_visto_segundos: duracion,
      completo: true
    })
  });
}
```

#### 3. Subir Nueva Historia

```javascript
async function subirHistoria(archivo, descripcion, destacada) {
  const formData = new FormData();
  formData.append('archivo', archivo);
  formData.append('descripcion', descripcion);
  formData.append('duracion_segundos', 5);
  formData.append('destacada', destacada);
  
  const response = await fetch(`${API_URL}/api/Historia/crear`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  
  const result = await response.json();
  
  if (result.respuesta === 'OK') {
    console.log('Historia creada:', result.data);
    // Actualizar UI
  }
}
```

#### 4. Ver Tus Historias con Estadísticas

```javascript
async function verMisHistorias() {
  const response = await fetch(`${API_URL}/api/Historia/mis-historias`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const data = await response.json();
  
  // Mostrar cada historia con:
  // - Imagen/Video
  // - Vistas totales
  // - Lista de quién la vio
  mostrarMisHistoriasConStats(data.data);
}
```

### Manejo de Errores

```javascript
async function handleHistoriaError(error) {
  if (error.status === 401) {
    // Token expirado, renovar o hacer login
    await renovarToken();
  } else if (error.status === 413) {
    // Archivo demasiado grande
    mostrarAlerta('El archivo es demasiado grande (máx 50MB)');
  } else {
    mostrarAlerta('Error al procesar la historia');
  }
}
```

---

## 📝 Notas Importantes

1. **Autenticación**: Todos los endpoints requieren JWT válido
2. **Expiración**: Historias normales expiran en 24h automáticamente
3. **Destacadas**: Las historias marcadas como destacadas NO expiran
4. **Vistas Propias**: No se registra cuando ves tu propia historia
5. **Miniaturas**: Se generan automáticamente para imágenes
6. **URLs**: Los archivos se sirven desde `/uploads/` en el servidor

## 🐛 Troubleshooting

### "Token inválido o expirado"
- Renovar el token haciendo login nuevamente

### "Extensión no permitida"
- Verificar que el archivo sea JPG, PNG, GIF, WEBP, MP4, MOV, AVI o WEBM

### "Archivo demasiado grande"
- Tamaño máximo: 50 MB
- Comprimir imagen/video antes de subir

### "No tienes permiso"
- Solo el dueño puede eliminar una historia

---

¿Necesitas más ayuda? Consulta la [documentación completa](README.md) o la [documentación de diseño](HISTORIAS_DESIGN.md).
