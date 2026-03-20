# 🚀 Quick Start - API SportMob Python

Guía rápida para levantar la API en menos de 5 minutos.

## ⚡ Inicio Rápido con Docker

```bash
# 1. Navega al directorio del proyecto
cd /Users/jrpech/GitHub/api-sportmob-py

# 2. Ejecuta el script de inicio
./start.sh

# O manualmente:
docker-compose up --build
```

¡Listo! La API estará disponible en:
- **API**: http://localhost:8000
- **Swagger**: http://localhost:8000/swagger
- **Docs**: http://localhost:8000/redoc

> **Nota**: La API se conecta a la base de datos MySQL remota configurada en `.env`

## 🔧 Desarrollo Local con MySQL

Si prefieres usar MySQL local en lugar del remoto:

```bash
./start-local.sh

# O manualmente:
docker-compose -f docker-compose.local.yml up --build
```

## 🧪 Probar el Login

### Con cURL:
```bash
curl -X POST http://localhost:8000/api/Login/auth \
  -H "Content-Type: application/json" \
  -d '{
    "usuario": "tu-email@example.com",
    "contrasena": "tu-password"
  }'
```

### Con script de prueba:
```bash
./test_api.sh
```

### Con Postman:
1. Ve a http://localhost:8000/swagger
2. Expande el endpoint `POST /api/Login/auth`
3. Click en "Try it out"
4. Ingresa las credenciales
5. Click en "Execute"

## 🔑 Verificar JWT

```bash
# Prueba la generación de tokens
python3 test_jwt.py
```

Esto mostrará:
- Token generado
- Claims decodificados
- Verificación de compatibilidad con .NET

## 🛑 Detener la API

```bash
# Detener y remover contenedores
docker-compose down

# Detener, remover y limpiar volúmenes
docker-compose down -v
```
### Base de Datos Remota (Configuración Actual)

```bash
# Conectar a la BD remota
mysql -h 146.190.144.229 -P 3306 -u remote-user -pSp0rtm0b2024 sportmob_v2
```

### Base de Datos Local (con docker-compose.local.yml)

```bash
# Desde tu máquina (puerto 3307)
mysql -h 127.0.0.1 -P 3307 -u root -prootroot sportmob_v2

# Desde el contenedor
docker-compose -f docker-compose.local.yml exec db mysql -uroot -prootroot sportmob_v2

# Ver logs de MySQL
docker-compose logs -f db
```

## 🗄️ Acceder a MySQL

```bash
# Desde tu máquina (puerto 3307)
mysql -h 127.0.0.1 -P 3307 -u root -prootroot pruebasliguilla

# Desde el contenedor
docker-compose exec db mysql -uroot -prootroot pruebasliguilla
```

## 💡 Problemas Comunes

### Puerto 8conectividad con el servidor remoto
ping 146.190.144.229

# Probar conexión directa
mysql -h 146.190.144.229 -P 3306 -u remote-user -pSp0rtm0b2024 sportmob_v2

# Ver logs de la API
docker-compose logs apibiar 8000 a 8001
```

### Base de datos no conecta
```bash
# Verificar que MySQL esté corriendo
docker-compose ps

# Ver logs de errores
docker-compose logs db
```

### Módulos Python no encontrados
```bash
# Reconstruir la imagen
docker-compose build --no-cache
docker-compose up
```

## 📚 Siguientes Pasos

1. Lee [README.md](README.md) para documentación completa
2. Lee [DEVELOPMENT.md](DEVELOPMENT.md) para guía de desarrollo
3. Importa [POSTMAN.md](POSTMAN.md) en Postman para pruebas
4. Revisa [reference/](reference/) para ver el código .NET original

## 🎯 Recordatorios

- ✅ JWT es 100% compatible con la API .NET
- ✅ La app móvil puede usar ambas APIs indistintamente
- ✅ Usa el mismo `JWT_SECRET_KEY` que .NET
- ✅ Los tokens generados por Python funcionan en .NET y viceversa

---

¿Necesitas ayuda? Revisa la documentación completa en [README.md](README.md)
