from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import BaseResponse, JugadorSchema, LoginJugadorRequest
from app.services.jugador_service import jugador_service

router = APIRouter(prefix="/api/Jugador", tags=["Jugador"])

#Metodo que se encarga de registrar a un jugador como usuario en sportmob mediante la app
@router.post("/registrarJugadorApp", response_model=BaseResponse)
def registrar_jugador(body: JugadorSchema,db: Session = Depends(get_db)):
    try:
        usuario_jugador = jugador_service.crear_jugador(db, body)

        return BaseResponse(
            respuesta="OK",
            mensaje="",
            data= usuario_jugador
        )
    except Exception as ex:
        error_mensaje = str(ex)
        if hasattr(ex, 'InnerException') and ex.InnerException:
            error_mensaje += str(ex.InnerException)
        
        return BaseResponse(
            respuesta="ERROR",
            mensaje=error_mensaje,
            data=None
        )

#Metodo para obtener un jugador por su correo electrónico, útil para login o validaciones previas al registro
@router.get("/obtenerJugadorPorCorreo", response_model=BaseResponse)
def obtener_jugador_por_correo(correo: str, db: Session = Depends(get_db)):
    try:
        jugador = jugador_service.obtener_jugador_por_correo(db, correo)        
        return BaseResponse(
            respuesta="OK",
            mensaje="",
            data=jugador
        )
    except Exception as ex:
        error_mensaje = str(ex)
        if hasattr(ex, 'InnerException') and ex.InnerException:
            error_mensaje += str(ex.InnerException)
        
        return BaseResponse(
            respuesta="ERROR",
            mensaje=error_mensaje,
            data=None
        )

#Metodo para hacer login de un jugador, este puede hacer login por correo o numero de telefono
@router.post("/loginJugador", response_model=BaseResponse)
def login_jugador(body: LoginJugadorRequest, db: Session = Depends(get_db)):
    try:
        usuario_jugador = jugador_service.login_jugador(db, body)

        return BaseResponse(
            respuesta="OK",
            mensaje="",
            data= usuario_jugador
        )
    except Exception as ex:
        error_mensaje = str(ex)
        if hasattr(ex, 'InnerException') and ex.InnerException:
            error_mensaje += str(ex.InnerException)
        
        return BaseResponse(
            respuesta="ERROR",
            mensaje=error_mensaje,
            data=None
        )               
