# Scripts de Base de Datos

Colección de scripts SQL para gestionar las tablas de historias.

## 📋 Archivos Disponibles

### `historias_schema.sql`
Crea todas las tablas necesarias para el sistema de historias:
- `historia` - Tabla principal de historias
- `historia_vista` - Tracking de visualizaciones
- `historia_reaccion` - Reacciones (opcional)

**Uso:**
```bash
# Desde línea de comandos
mysql -h 146.190.144.229 -P 3306 -u remote-user -pSp0rtm0b2024 sportmob_v2 < database/historias_schema.sql

# Desde MySQL client
source database/historias_schema.sql;
```

### `drop_historias.sql`
Elimina todas las tablas de historias. 

⚠️ **CUIDADO**: Esto borrará todos los datos.

**Uso:**
```bash
mysql -h 146.190.144.229 -P 3306 -u remote-user -pSp0rtm0b2024 sportmob_v2 < database/drop_historias.sql
```

### `seed_historias.sql`
Inserta datos de prueba para desarrollo.

**Nota**: Requiere que existan usuarios en la tabla `usuario`.

**Uso:**
```bash
mysql -h 146.190.144.229 -P 3306 -u remote-user -pSp0rtm0b2024 sportmob_v2 < database/seed_historias.sql
```

## 🚀 Setup Inicial

Para configurar las tablas por primera vez:

```bash
# 1. Crear las tablas
mysql -h 146.190.144.229 -P 3306 -u remote-user -pSp0rtm0b2024 sportmob_v2 < database/historias_schema.sql

# 2. (Opcional) Insertar datos de prueba
mysql -h 146.190.144.229 -P 3306 -u remote-user -pSp0rtm0b2024 sportmob_v2 < database/seed_historias.sql
```

## 📊 Ver Estructura

```sql
-- Ver estructura de las tablas
DESCRIBE historia;
DESCRIBE historia_vista;
DESCRIBE historia_reaccion;

-- Ver estadísticas
SELECT 
    'Historias totales' as descripcion, COUNT(*) as total FROM historia
UNION ALL
SELECT 'Historias activas', COUNT(*) FROM historia WHERE activa = TRUE
UNION ALL
SELECT 'Historias destacadas', COUNT(*) FROM historia WHERE destacada = TRUE;
```

## 🔄 Reset Completo

Si necesitas empezar de cero:

```bash
# 1. Eliminar tablas
mysql -h 146.190.144.229 -P 3306 -u remote-user -pSp0rtm0b2024 sportmob_v2 < database/drop_historias.sql

# 2. Recrear tablas
mysql -h 146.190.144.229 -P 3306 -u remote-user -pSp0rtm0b2024 sportmob_v2 < database/historias_schema.sql
```

## 📝 Notas

- Las tablas usan `ON DELETE CASCADE`, así que eliminar un usuario eliminará sus historias automáticamente
- Las historias destacadas tienen `fecha_expiracion = NULL`
- Las historias normales expiran en 24 horas por defecto
- El trigger `actualizar_vistas_totales` incrementa automáticamente el contador al registrar una vista
