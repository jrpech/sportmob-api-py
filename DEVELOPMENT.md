# Notas de Desarrollo - API SportMob Python

## 🔑 Puntos Clave de Compatibilidad JWT

### Configuración Crítica

Los siguientes valores **DEBEN** ser idénticos entre Python y .NET:

```python
# Python (.env)
JWT_SECRET_KEY=VaibhavBhapkarVaibhavBhapkar
JWT_ISSUER=https://localhost:5001/
JWT_AUDIENCE=https://localhost:5001/
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=43200
```

```csharp
// .NET (appsettings.json)
"Jwt": {
  "SecretKey": "VaibhavBhapkarVaibhavBhapkar",
  "Issuer": "https://localhost:5001/",
  "Audience": "https://localhost:5001/"
}
```

### Claims en el Token

Ambas APIs generan los mismos claims:

| Claim | Descripción | Ejemplo |
|-------|-------------|---------|
| `sub` | Email del usuario | "usuario@example.com" |
| `fullName` | Nombre completo | "Juan Pérez" |
| `usuario` | Email (duplicado) | "usuario@example.com" |
| `id` | ID del usuario | "1" |
| `jti` | GUID único | "550e8400-e29b-41d4-a716-446655440000" |
| `exp` | Timestamp expiración | 1708473600 |
| `iss` | Issuer | "https://localhost:5001/" |
| `aud` | Audience | "https://localhost:5001/" |

## 🔐 Manejo de Contraseñas

### Verificación Actual

El código incluye dos métodos de verificación:

1. **Comparación directa** - Si las contraseñas están en texto plano
2. **SHA1 + Base64** - Compatible con `Cifrado.cs` de .NET

```python
def verify_password(plain_password: str, stored_password: str) -> bool:
    # Método 1: Comparación directa
    if plain_password == stored_password:
        return True
    
    # Método 2: SHA1 con Unicode encoding + Base64
    hashed = hashlib.sha1(plain_password.encode('utf-16-le')).digest()
    hashed_b64 = base64.b64encode(hashed).decode('utf-8')
    if hashed_b64 == stored_password:
        return True
    
    return False
```

### ⚠️ Recomendaciones de Seguridad

- Las contraseñas en texto plano son un riesgo de seguridad
- SHA1 está desactuado y NO es seguro para nuevas implementaciones
- **Recomendación**: Migrar a bcrypt o Argon2

#### Migración a bcrypt

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

## 📊 Estructura de la Base de Datos

### Tabla usuario

```sql
CREATE TABLE usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    correo VARCHAR(255) UNIQUE,
    contrasenia VARCHAR(255),  -- 'ñ' en lugar de 'ñ'
    telefono VARCHAR(50),
    estado VARCHAR(100),
    foto VARCHAR(500),
    origen VARCHAR(100)
);
```

### Diferencias con .NET

- Python usa `contrasenia` (idéntico a .NET)
- El modelo de .NET incluye más campos que aún no están en todas las respuestas
- Asegúrate de que los nombres de columnas coincidan exactamente

## 🚀 Agregar Nuevos Endpoints

### 1. Crear Router

Crea un nuevo archivo en `app/routers/`:

```python
# app/routers/equipo.py
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.schemas import BaseResponse

router = APIRouter(prefix="/api/Equipo", tags=["Equipo"])

@router.get("/lista", response_model=BaseResponse)
async def get_equipos():
    """Lista todos los equipos"""
    # Implementar lógica
    return BaseResponse(
        respuesta="OK",
        mensaje="",
        data=[]
    )
```

### 2. Registrar Router en main.py

```python
from app.routers import login, equipo

app.include_router(login.router)
app.include_router(equipo.router)  # Agregar esta línea
```

### 3. Proteger con Autenticación (Opcional)

```python
@router.get("/lista", response_model=BaseResponse)
async def get_equipos(current_user: dict = Depends(get_current_user)):
    # Solo usuarios autenticados pueden acceder
    return BaseResponse(...)
```

## 🗄️ Trabajar con la Base de Datos

### Crear Nuevo Modelo

```python
# app/models.py
class Equipo(Base):
    __tablename__ = "equipo"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(255))
    logo = Column(String(500))
    # ... más campos
```

### Query en el Endpoint

```python
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Equipo

@router.get("/lista")
async def get_equipos(db: Session = Depends(get_db)):
    equipos = db.query(Equipo).all()
    return BaseResponse(
        respuesta="OK",
        data=[eq.__dict__ for eq in equipos]
    )
```

## 🐛 Debugging

### Ver Logs de Docker

```bash
# Ver logs en tiempo real
docker-compose logs -f api

# Ver últimas 100 líneas
docker-compose logs --tail=100 api

# Ver logs de MySQL
docker-compose logs -f db
```

### Conectar a MySQL desde el contenedor

```bash
docker-compose exec db mysql -uroot -prootroot pruebasliguilla

# Una vez dentro:
SHOW TABLES;
DESCRIBE usuario;
SELECT * FROM usuario LIMIT 5;
```

### Ejecutar Python dentro del contenedor

```bash
docker-compose exec api bash

# Dentro del contenedor:
python test_jwt.py
python -m pytest
```

## 🔄 Migración de Endpoints desde .NET

Para cada controlador en .NET, sigue estos pasos:

### 1. Analizar el Controller .NET

```csharp
// reference/Controllers/EquipoController.cs
[Route("api/[controller]")]
public class EquipoController : ControllerBase
{
    [HttpGet]
    [Route("lista")]
    public IActionResult GetEquipos() { ... }
}
```

### 2. Crear Router equivalente en Python

```python
# app/routers/equipo.py
router = APIRouter(prefix="/api/Equipo", tags=["Equipo"])

@router.get("/lista", response_model=BaseResponse)
async def get_equipos(): ...
```

### 3. Migrar la Lógica

- Traduce queries de NHibernate a SQLAlchemy
- Mantén el mismo formato de respuesta
- Usa `BaseResponse` para compatibilidad

### 4. Probar

```bash
# Test manual
curl -X GET http://localhost:8000/api/Equipo/lista

# Comparar con .NET
curl -X GET https://localhost:5001/api/Equipo/lista
```

## 📦 Dependencias Importantes

### PyJWT vs python-jose

Usamos **PyJWT** porque:
- Es más simple y directo
- Compatible nativamente con el formato de .NET
- Menor overhead

### SQLAlchemy

ORM para Python, equivalente a NHibernate de .NET:

```python
# .NET NHibernate
var usuario = _session.Query<Usuario>()
    .Where(x => x.correo == email)
    .FirstOrDefault();

# Python SQLAlchemy
usuario = db.query(Usuario)\
    .filter(Usuario.correo == email)\
    .first()
```

## ⚡ Performance Tips

### Connection Pooling

Ya configurado en `app/database.py`:

```python
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,      # Verifica conexiones antes de usar
    pool_recycle=3600,       # Recicla conexiones cada hora
    echo=settings.DEBUG      # Log SQL queries en dev
)
```

### Async vs Sync

FastAPI soporta endpoints async, pero SQLAlchemy por defecto es sincrónico.

Para usar async SQLAlchemy:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine(
    "mysql+aiomysql://...",
    echo=True
)
```

## 🧪 Testing

### Estructura de Tests (Futuro)

```
tests/
├── __init__.py
├── conftest.py          # Fixtures compartidos
├── test_auth.py         # Tests de autenticación
├── test_login.py        # Tests del endpoint login
└── test_jwt.py          # Tests de generación JWT
```

### Ejemplo de Test

```python
# tests/test_login.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/api/Login/auth",
        json={
            "usuario": "test@example.com",
            "contrasena": "password"
        }
    )
    assert response.status_code == 200
    assert "token" in response.json()["data"]
```

## 📝 Checklist para Nuevos Endpoints

- [ ] Crear router en `app/routers/`
- [ ] Crear modelos si son necesarios
- [ ] Crear schemas de request/response
- [ ] Implementar lógica de negocio
- [ ] Agregar validaciones
- [ ] Registrar router en `main.py`
- [ ] Probar con cURL o Postman
- [ ] Actualizar documentación
- [ ] Comparar respuesta con API .NET
- [ ] Verificar compatibilidad de JWT si usa auth

## 🔒 Seguridad Checklist

- [ ] Validar entrada de usuarios
- [ ] Sanitizar queries SQL (SQLAlchemy lo hace automáticamente)
- [ ] Verificar permisos en endpoints protegidos
- [ ] Rate limiting (pendiente de implementar)
- [ ] Logging de intentos de login fallidos
- [ ] HTTPS en producción
- [ ] Rotar JWT_SECRET_KEY periódicamente
- [ ] No exponer información sensible en errores

## 📚 Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [PyJWT Docs](https://pyjwt.readthedocs.io/)
- [Docker Compose Docs](https://docs.docker.com/compose/)

---

**Última actualización**: Marzo 2026
