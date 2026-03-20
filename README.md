# API SportMob Python

API REST desarrollada en Python con FastAPI, compatible con la autenticación JWT de la API .NET existente.

## 🎯 Características

- ✅ **Autenticación JWT compatible** con el proyecto .NET en `/reference`
- ✅ **Docker** para desarrollo y producción
- ✅ **FastAPI** - Framework moderno y rápido para Python
- ✅ **MySQL** - Base de datos compatible con el proyecto .NET
- ✅ **Swagger UI** - Documentación automática de la API
- ✅ **CORS** configurado para la app móvil
- ✅ **Mismo formato de respuestas** que la API .NET
- ✅ **Sistema de Historias** - Stories tipo Instagram con almacenamiento local/S3
- ✅ **Procesamiento de imágenes** - Generación automática de miniaturas
- ✅ **Soporte de video** - Videos cortos hasta 30 segundos

## 🔐 Compatibilidad JWT

La API genera tokens JWT **100% compatibles** con la API .NET:

- **Secret Key**: `VaibhavBhapkarVaibhavBhapkar`
- **Issuer**: `https://localhost:5001/`
- **Audience**: `https://localhost:5001/`
- **Algoritmo**: HS256
- **Expiración**: 43200 minutos (30 días)
- **Claims**: sub, fullName, usuario, id, jti

Esto permite que la aplicación móvil pueda usar ambas APIs indistintamente.

## 📁 Estructura del Proyecto

```
api-sportmob-py/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuración de la aplicación
│   ├── database.py        # Conexión a base de datos
│   ├── models.py          # Modelos SQLAlchemy (Usuario, Historia, etc.)
│   ├── schemas.py         # Esquemas Pydantic
│   ├── auth.py            # Generación y validación JWT
│   ├── dependencies.py    # Dependencias de autenticación
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── login.py       # Endpoint de autenticación
│   │   └── historia.py    # Endpoints de historias/stories
│   ├── services/
│   │   ├── __init__.py
│   │   ├── storage_service.py   # Servicio de almacenamiento (local/S3)
│   │   └── historia_service.py  # Lógica de negocios de historias
│   └── utils/
│       ├── __init__.py
│       └── image_utils.py       # Procesamiento de imágenes
├── database/
│   ├── historias_schema.sql     # Script de creación de tablas
│   ├── drop_historias.sql       # Script de limpieza
│   ├── seed_historias.sql       # Datos de prueba
│   └── README.md                # Documentación de BD
├── uploads/                     # Almacenamiento local de archivos
│   └── historias/
├── reference/                   # Proyecto .NET de referencia
├── main.py                      # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias Python
├── Dockerfile                   # Imagen Docker
├── docker-compose.yml           # Orquestación de servicios
├── docker-compose.local.yml     # Docker con MySQL local
├── .env                         # Variables de entorno
├── README.md                    # Este archivo
├── HISTORIAS_GUIA.md            # Guía completa del sistema de historias
└── HISTORIAS_DESIGN.md          # Documentación de diseño de historias
```

## 🚀 Inicio Rápido

### Opción 1: Con Base de Datos Remota (Producción)

La configuración actual en `.env` apunta a una base de datos MySQL remota.

1. **Verificar variables de entorno en `.env`**
   ```bash
   # Las credenciales de BD remota ya están configuradas
   DB_HOST=146.190.144.229
   DB_NAME=sportmob_v2
   DB_USER=remote-user
   DB_PASSWORD=Sp0rtm0b2024
   ```

2. **Levantar la API con Docker**
   ```bash
   ./start.sh
   
   # O manualmente:
   docker-compose up --build
   ```
3: Sin Docker (Desarrollo local)

1. **Crear entorno virtual**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verificar variables de entorno en `.env`**
   ```bash
   # Asegúrate de que las credenciales de BD sean correctas

Esto levantará:
- API en puerto 8000
- MySQL en puerto 3307

### Opción 2: Sin Docker (Desarrollo local)

1. **Crear entorno virtual**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

### Historias (Stories)

- **POST `/api/Historia/crear`** - Crear nueva historia (imagen o video)
- **GET `/api/Historia/feed`** - Obtener feed de historias de todos los usuarios
- **GET `/api/Historia/mis-historias`** - Ver tus historias con estadísticas
- **POST `/api/Historia/{id}/ver`** - Marcar historia como vista
- **DELETE `/api/Historia/{id}`** - Eliminar una historia
- **GET `/api/Historia/{id}/vistas`** - Ver quién vio tu historia

📖 **Guía completa**: Ver [HISTORIAS_GUIA.md](HISTORIAS_GUIA.md) para ejemplos detallados

---

### Detalles de Autenticación

#### POST `/api/Login/auth`

3. **Configurar variables de entorno**
   ```bash
   # Edita .env para apuntar a tu base de datos local
   # Cambia DB_HOST de "db" a "localhost"
   ```

4. **Ejecutar la aplicación**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📋 Endpoints Disponibles

### Autenticación

#### POST `/api/Login/auth`

Autentica un usuario y devuelve un token JWT.

**Request:**
```json
{
  "usuario": "usuario@example.com",
  "contrasena": "password123"
}
```

**Response Exitoso:**
```json
{
  "respuesta": "OK",
  "mensaje": "",
  "data": {
    "id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "correo": "usuario@example.com",
    "telefono": "1234567890",
    "estado": "Activo",
    "foto": null,
    "origen": "app",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Response Error:**
```json
{
  "respuesta": "ERROR",
  "mensaje": "Usuario y/o contraseña invalidos",
  "data": null
}
```

### Health Check

#### GET `/health`

Verifica el estado de la API.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🔧 Configuración

El archivo `.env` contiene todas las configuraciones:

```env
# JWT Configuration (DEBE SER IDENTICA A LA DE .NET)
JWT_SECRET_KEY=VaibhavBhapkarVaibhavBhapkar
JWT_ISSUER=https://localhost:5001/
JWT_AUDIENCE=https://localhost:5001/
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=43200

# Database Configuration
DB_HOST=db               - MySQL Remoto
DB_HOST=146.190.144.229
DB_PORT=3306
DB_NAME=sportmob_v2
DB_USER=remote-user
DB_PASSWORD=Sp0rtm0b2024
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS Origins
CORS_ORIGINS=http://localhost:51297,http://tamara.digimob.mx
```

## 🔒 Seguridad

### Contraseñas

La API soporta dos métodos de verificación de contraseñas:

1. **Comparación directa** - Si las contraseñas están en texto plano
2. **SHA1 + Base64** - Compatible con el método `Cifrado.cs` de .NET

El método se detecta automáticamente en `app/routers/login.py`.

### Recomendaciones

- ⚠️ Cambia `JWT_SECRET_KEY` en producción
- ⚠️ Usa HTTPS en producción
- ⚠️ Implementa rate limiting
- ⚠️ Hashea las contraseñas (bcrypt o Argon2)

## 🗄️ Base de Datos

La API usa MySQL y es compatible con la base de datos del proyecto .NET.
está configurada para conectarse a una base de datos MySQL remota.

### Configuración Actual

```env
DB_HOST=146.190.144.229
DB_PORT=3306
DB_NAME=sportmob_v2
DB_USER=remote-user
DB_PASSWORD=Sp0rtm0b2024
```

### Desarrollo Local

Si prefieres usar MySQL local para desarrollo:

```bash
# Usa docker-compose.local.yml
./start-local.sh
```

### Conexión Directa a MySQL Remoto

```bash
mysql -h 146.190.144.229 -P 3306 -u remote-user -pSp0rtm0b2024 sportmob_v2
``
## 📚 Documentación Interactiva

Una vez que la API esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/swagger
  - Interfaz interactiva para probar los endpoints
  
- **ReDoc**: http://localhost:8000/redoc
  - Documentación alternativa más detallada

## 🛠️ Comandos Útiles

### Docker

```bash (solo API, BD remota)
docker-compose up

# Levantar con MySQL local para desarrollo
docker-compose -f docker-compose.local.yml up

# Levantar en background
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Detener servicios
docker-compose down

# Reconstruir imágenes
docker-compose up --build

# Acceder al contenedor
docker-compose exec api bash
docker-compose exec db mysql -uroot -prootroot pruebasliguilla
```

### Python

```bash
# Instalar nuevas dependencias
pip install nombre-paquete
pip freeze > requirements.txt

# Ejecutar tests (si los agregas)
pytest

# Linter y formato
black app/
flake8 app/
```

## 🧪 Testing

Para probar el endpoint de login con curl:

```bash
curl -X POST http://localhost:8000/api/Login/auth \
  -H "Content-Type: application/json" \
  -d '{
    "usuario": "usuario@example.com",
    "contrasena": "password123"
  }'
```

## 🐛 Solución de Problemas

### Error de conexión a base de datos
el servidor MySQL remoto esté accesible
- Revisa las credenciales en `.env`
- Verifica que el firewall permita conexiones desde tu IP
- Prueba la conexión directa con:
  ```bash
  mysql -h 146.190.144.229 -P 3306 -u remote-user -pSp0rtm0b2024 sportmob_v2
  ```
- Si usas Docker, asegúrate de que el contenedor `db` esté levantado

### Error "Module not found"

```bash
pip install -r requirements.txt
```

### Puerto 8000 ya en uso

Cambia el puerto en `.env` o en `docker-compose.yml`

## 🔄 Comparación con API .NET

| Característica | .NET API | Python API |
|---------------|----------|------------|
| Framework | ASP.NET Core | FastAPI |
| Puerto | 5001 | 8000 |
| Documentación | Swagger | Swagger + ReDoc |
| JWT Secret | VaibhavBhapkar... | **Idéntico** |
| JWT Claims | sub, fullName, usuario, id, jti | **Idéntico** |
| Formato Response | BaseResponse | **Idéntico** |
| Endpoint Login | `/api/Login/auth` | **Idéntico** |

## 📝 TODOs / Próximos Pasos

- [ ] Agregar más endpoints (Equipos, Torneos, etc.)
- [ ] Implementar tests unitarios
- [ ] Agregar middleware de autenticación para proteger endpoints
- [ ] Implementar rate limiting
- [ ] Agregar logging estructurado
- [ ] Crear script de migración de datos
- [ ] Dockerizar la API .NET también
- [ ] Configurar CI/CD

## 👥 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto es privado y confidencial.

## 🆘 Soporte

Si tienes problemas o preguntas, contacta al equipo de desarrollo.

---

**Nota**: Este proyecto fue creado para ser compatible con la API .NET existente. Cualquier cambio en la configuración JWT debe sincronizarse con ambas APIs para mantener la compatibilidad.
