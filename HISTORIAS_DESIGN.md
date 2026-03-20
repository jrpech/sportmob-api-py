# 🎨 Documentación de Diseño - Sistema de Historias

Documentación técnica sobre el diseño e implementación del sistema de historias (stories) tipo Instagram.

## 📐 Arquitectura General

### Capas de la Aplicación

```
┌─────────────────────────────────────────┐
│          API Layer (FastAPI)            │
│  /api/Historia/* - RouterHistoria       │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│        Service Layer                    │
│  - HistoriaService (lógica de negocio)  │
│  - StorageService (almacenamiento)      │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│        Data Access Layer                │
│  - Models (SQLAlchemy ORM)              │
│  - Schemas (Pydantic validation)        │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│          MySQL Database                 │
│  - historia, historia_vista,            │
│    historia_reaccion                    │
└─────────────────────────────────────────┘
```

---

## 🗄️ Modelo de Datos

### Diagrama ER

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│    usuario      │         │     historia     │         │ historia_vista  │
├─────────────────┤         ├──────────────────┤         ├─────────────────┤
│ id (PK)         │◄───────┤ usuario_id (FK)  │────────►│ historia_id (FK)│
│ nombre          │         │ id (PK)          │         │ usuario_id (FK) │
│ apellido        │         │ tipo             │         │ fecha_vista     │
│ correo          │         │ url_archivo      │         │ tiempo_visto    │
│ ...             │         │ descripcion      │         │ completo        │
└─────────────────┘         │ fecha_creacion   │         └─────────────────┘
                            │ fecha_expiracion │
                            │ destacada        │                ▲
                            │ vistas_totales   │                │
                            │ ancho / alto     │                │
                            │ duracion_seg     │                │
                            └──────────────────┘                │
                                     │                          │
                                     │                          │
                                     ▼                          │
                            ┌──────────────────┐                │
                            │historia_reaccion │────────────────┘
                            ├──────────────────┤
                            │ historia_id (FK) │
                            │ usuario_id (FK)  │
                            │ tipo_reaccion    │
                            │ fecha_reaccion   │
                            └──────────────────┘
```

### Tabla: `historia`

**Propósito**: Almacenar las historias (fotos/videos) de los usuarios.

**Campos Principales**:
- `tipo`: ENUM('imagen', 'video') - Tipo de contenido
- `destacada`: BOOLEAN - Si no expira (featured story)
- `fecha_expiracion`: DATETIME NULL - NULL si es destacada, +24h si es normal
- `vistas_totales`: INT - Contador actualizado por trigger

**Índices Importantes**:
- `idx_usuario`: Para obtener historias de un usuario
- `idx_fecha_creacion`: Para ordenar por más reciente
- `idx_activa`: Filtrar solo historias activas
- `idx_destacada`: Separar destacadas de normales

### Tabla: `historia_vista`

**Propósito**: Tracking de quién vio cada historia.

**Campos Principales**:
- `completo`: BOOLEAN - Si vio la historia completa
- `tiempo_visto_segundos`: INT - Cuánto tiempo la vio

**Constraint Único**: (historia_id, usuario_id) - No duplicar vistas

### Tabla: `historia_reaccion`

**Propósito**: Reacciones a las historias (preparado para futuro).

**Tipos de Reacción**:
- `me_gusta`, `me_encanta`, `me_divierte`, `me_asombra`, `me_entristece`, `me_enoja`

---

## 🔧 Decisiones de Diseño

### 1. **Historias Destacadas vs Normales**

**Decisión**: Usar un flag `destacada` en lugar de tablas separadas.

**Razón**:
- ✅ Simplifica queries (solo un WHERE destacada = true)
- ✅ No duplica datos
- ✅ Evita problemas de sincronización
- ✅ Fácil cambiar de normal a destacada

**Implementación**:
```python
def calcular_fecha_expiracion(destacada: bool) -> Optional[datetime]:
    if destacada:
        return None  # No expira
    return datetime.utcnow() + timedelta(hours=24)
```

### 2. **Almacenamiento Abstracto (Local / S3)**

**Decisión**: Crear `StorageService` con interfaz única para local y S3.

**Razón**:
- ✅ Fácil migración de local a S3
- ✅ Testing sin dependencias de AWS
- ✅ Puede usar ambos simultáneamente (transición gradual)
- ✅ No acopla la lógica de negocio al almacenamiento

**Interfaz**:
```python
class StorageService:
    async def guardar_archivo(...)      # Guarda en local o S3
    def obtener_url_publica(...)        # URL según backend
    async def eliminar_archivo(...)      # Elimina de local o S3
    def _organizar_por_fecha(...)       # estructura: YYYY/MM/DD
```

**Configuración Actual**: Local en `/app/uploads/historias/`  
**Migración a S3**: Cambiar `STORAGE_TYPE=s3` en `.env`

### 3. **Procesamiento de Imágenes**

**Decisión**: Generar miniaturas automáticamente con Pillow.

**Razón**:
- ✅ Reduce ancho de banda en el feed (mostrar solo thumbnails)
- ✅ Mejora experiencia en conexiones lentas
- ✅ Tamaño fijo de 300x400px mantiene aspecto consistente

**Implementación**:
```python
def crear_miniatura(imagen: Image.Image) -> Image.Image:
    imagen.thumbnail((300, 400), Image.LANCZOS)
    return imagen
```

**Estructura de Archivos**:
```
uploads/
└── historias/
    ├── 2026/03/20/
    │   ├── historia_20260320_123456_abc12345.jpg     # Original
    │   └── ...
    └── miniaturas/
        └── 2026/03/20/
            └── thumb_historia_20260320_123456_abc12345.jpg
```

### 4. **Tracking de Vistas**

**Decisión**: Guardar cada vista individualmente en tabla separada.

**Razón**:
- ✅ Permite ver **quién** vio la historia
- ✅ Permite analizar **cuándo** la vieron
- ✅ Saber si la vieron **completa** o no
- ✅ El contador en `historia.vistas_totales` se actualiza con trigger

**Query Optimizado**:
```sql
-- Vistas de una historia específica
SELECT u.nombre, hv.fecha_vista, hv.completo
FROM historia_vista hv
JOIN usuario u ON hv.usuario_id = u.id
WHERE hv.historia_id = ?
ORDER BY hv.fecha_vista DESC;
```

### 5. **Formato de Respuesta Compatible con .NET**

**Decisión**: Usar el mismo formato que la API .NET existente.

**Razón**:
- ✅ La app móvil funciona sin cambios
- ✅ Ambas APIs intercambiables
- ✅ Desarrollo frontend más simple

**Formato**:
```json
{
  "respuesta": "OK" | "ERROR",
  "mensaje": "...",
  "data": { ... }
}
```

### 6. **Validación de Videos**

**Decisión**: Validar duración máxima de 30 segundos.

**Razón**:
- ✅ Reduce uso de almacenamiento
- ✅ Mejora experiencia de usuario (historias cortas)
- ✅ Compatible con Instagram (15-60s actualmente)

**Pendiente**: Implementar extracción de thumbnail de video (actualmente solo valida tamaño).

### 7. **Trigger para Actualizar Contador**

**Decisión**: Usar trigger SQL en lugar de Python para actualizar `vistas_totales`.

**Razón**:
- ✅ Garantiza consistencia (atómico en BD)
- ✅ Mejor rendimiento (no hace query extra)
- ✅ No depende de código Python

**Trigger**:
```sql
CREATE TRIGGER actualizar_vistas_totales
AFTER INSERT ON historia_vista
FOR EACH ROW
UPDATE historia 
SET vistas_totales = vistas_totales + 1
WHERE id = NEW.historia_id;
```

### 8. **Soft Delete vs Hard Delete**

**Decisión**: Hard delete (eliminar completamente).

**Razón**:
- ✅ Ahorra espacio en disco
- ✅ Cumple con expectativas de usuario (borrado permanente)
- ✅ Menos complejidad en queries

**Implementación**: Al eliminar, se borran:
1. Registro de `historia`
2. Todos los registros de `historia_vista` (CASCADE)
3. Todos los registros de `historia_reaccion` (CASCADE)
4. Archivo físico en disco/S3

---

## 🔐 Seguridad

### Autenticación

Todos los endpoints requieren JWT válido:

```python
@router.post("/crear")
async def crear_historia(
    current_user: dict = Depends(get_current_user),  # JWT obligatorio
    ...
):
```

### Autorización

**Regla**: Solo el dueño puede eliminar su historia.

```python
if historia.usuario_id != current_user["id"]:
    raise HTTPException(
        status_code=403,
        detail="No tienes permiso para eliminar esta historia"
    )
```

### Validación de Archivos

1. **Extensión**: Solo formatos permitidos (JPG, PNG, GIF, WEBP, MP4, MOV, AVI, WEBM)
2. **Tamaño**: Máximo 50 MB
3. **Tipo MIME**: Validado con `python-magic`
4. **Nombre sanitizado**: Sin caracteres peligrosos

```python
def sanitizar_nombre_archivo(nombre: str) -> str:
    nombre = nombre.replace(" ", "_")
    nombre = "".join(c for c in nombre if c.isalnum() or c in "._-")
    return nombre
```

---

## 🚀 Performance

### Optimizaciones Implementadas

1. **Índices en BD**:
   - `idx_usuario` - Para queries por usuario
   - `idx_fecha_creacion` - Para ordenar por fecha
   - `idx_activa` - Filtrar solo activas
   - Índice compuesto en `historia_vista(historia_id, usuario_id)`

2. **Eager Loading**:
   ```python
   query = query.options(
       joinedload(Historia.usuario),
       joinedload(Historia.vistas)
   )
   ```

3. **Paginación en Feed**:
   ```python
   .limit(limite)  # Default 50 usuarios
   ```

4. **Miniaturas**:
   - Feed solo carga thumbnails (300x400)
   - Full resolution solo al ver la historia

5. **Async I/O**:
   ```python
   async with aiofiles.open(ruta_completa, 'wb') as f:
       await f.write(contenido)
   ```

### Métricas Esperadas

- **Creación de historia**: ~500-1000ms (con thumbnail)
- **Feed (50 usuarios)**: ~200-400ms
- **Marcar como vista**: ~50-100ms
- **Tamaño de thumbnail**: ~30-50KB (vs 2-5MB original)

---

## 🔄 Flujo de Datos

### 1. Crear Historia

```
Usuario -> POST /crear (multipart/form-data)
    │
    ├─► Validar JWT (get_current_user)
    │
    ├─► HistoriaService.crear_historia()
    │   │
    │   ├─► Validar archivo (extensión, tamaño, MIME)
    │   │
    │   ├─► StorageService.guardar_archivo()
    │   │   ├─► Sanitizar nombre
    │   │   ├─► Organizar por fecha (YYYY/MM/DD)
    │   │   └─► Guardar en /uploads/historias/
    │   │
    │   ├─► image_utils.crear_miniatura()
    │   │   └─► Guardar en /uploads/historias/miniaturas/
    │   │
    │   ├─► Insertar en BD (tabla historia)
    │   │
    │   └─► Retornar HistoriaResponse
    │
    └─► Response con URL pública
```

### 2. Ver Feed

```
Usuario -> GET /feed?limite=50
    │
    ├─► Validar JWT
    │
    ├─► HistoriaService.obtener_historias_activas()
    │   │
    │   ├─► Query historias activas (fecha_expiracion > now OR destacada)
    │   │
    │   ├─► Agrupar por usuario_id
    │   │
    │   ├─► Ordenar por fecha_creacion DESC
    │   │
    │   ├─► Check cuáles ya vio (historia_vista)
    │   │
    │   └─► Formatear respuesta
    │
    └─► Response agrupado por usuario
```

### 3. Marcar como Vista

```
Usuario -> POST /{id}/ver
    │
    ├─► Validar JWT
    │
    ├─► Verificar que no sea su propia historia
    │
    ├─► HistoriaService.marcar_como_vista()
    │   │
    │   ├─► Verificar que no exista (historia_vista)
    │   │
    │   ├─► INSERT INTO historia_vista
    │   │
    │   └─► Trigger actualiza historia.vistas_totales
    │
    └─► Response confirmación
```

---

## 🧪 Testing

### Casos de Prueba Recomendados

#### Unit Tests

```python
def test_crear_historia_imagen():
    """Debe crear historia con imagen válida"""
    
def test_crear_historia_destacada():
    """Historia destacada debe tener fecha_expiracion = NULL"""
    
def test_validar_duracion_video():
    """Debe rechazar videos >30s"""
    
def test_sanitizar_nombre_archivo():
    """Debe limpiar caracteres peligrosos"""
```

#### Integration Tests

```python
def test_flow_completo():
    """
    1. Login -> obtener token
    2. Crear historia
    3. Ver feed (debe aparecer la historia)
    4. Otro usuario marca como vista
    5. Ver vistas (debe aparecer el usuario)
    6. Eliminar historia
    """
```

#### Load Tests

```bash
# Test con Apache Bench
ab -n 1000 -c 10 \
   -H "Authorization: Bearer TOKEN" \
   http://localhost:8000/api/Historia/feed
```

---

## 📦 Deployment

### Variables de Entorno Requeridas

```env
# Almacenamiento
UPLOAD_DIR=/app/uploads
MAX_FILE_SIZE_MB=50
ALLOWED_EXTENSIONS_IMAGE=jpg,jpeg,png,gif,webp
ALLOWED_EXTENSIONS_VIDEO=mp4,mov,avi,webm

# Historias
HISTORIA_EXPIRACION_HORAS=24
HISTORIA_VIDEO_MAX_SEGUNDOS=30

# S3 (opcional, para migración)
STORAGE_TYPE=local  # o 's3'
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
S3_BUCKET_NAME=
```

### Migrar a S3

1. Crear bucket en AWS S3
2. Configurar IAM user con permisos
3. Actualizar `.env`:
   ```env
   STORAGE_TYPE=s3
   AWS_ACCESS_KEY_ID=AKIA...
   AWS_SECRET_ACCESS_KEY=...
   AWS_REGION=us-east-1
   S3_BUCKET_NAME=sportmob-historias
   ```
4. Reiniciar API
5. (Opcional) Migrar archivos existentes con script

---

## 🔮 Roadmap Futuro

### Features Pendientes

- [ ] **Video Thumbnail Extraction**: Extraer frame del video para thumbnail
- [ ] **Reacciones**: Implementar endpoint para reaccionar a historias
- [ ] **Responder Historias**: Permitir responder con mensaje/foto
- [ ] **Analytics**: Dashboard de estadísticas de historias
- [ ] **Notificaciones Push**: Avisar cuando alguien sube historia
- [ ] **Stories Destacadas por Tag**: Agrupar destacadas por categoría
- [ ] **Transcoding de Video**: Convertir videos a formato optimizado
- [ ] **CDN Integration**: Servir archivos desde CDN para mejor performance

### Optimizaciones Futuras

- [ ] **Cache de Feed**: Redis para cachear feed por 30s
- [ ] **Compresión de Imágenes**: WebP con mejor ratio
- [ ] **Lazy Loading**: Cargar historias bajo demanda
- [ ] **Background Jobs**: Procesar videos en background con Celery

---

## 📚 Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pillow - Image Processing](https://pillow.readthedocs.io/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [AWS S3 Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3.html)

---

**Última actualización**: Marzo 2026  
**Versión**: 1.0.0  
**Mantenedor**: @jrpech
