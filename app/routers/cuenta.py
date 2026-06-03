from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import BaseResponse
from app.models import Cuenta


router = APIRouter(prefix="/api/Cuenta", tags=["Cuenta"])


#Este metodo se encarga de recuperar los detalles de la cuenta por el parametro token
@router.get("/getCuentaToken",response_model=BaseResponse)
async def get_cuenta_token(token: str, db: Session = Depends(get_db)):
    try:
        #Buscamos la cuenta mediante el token que estamos recibiendo
        cuenta = db.query(Cuenta).filter(Cuenta.token == token).first()

        if cuenta is None:
            return BaseResponse(
                respuesta="ERROR",
                mensaje= "No se encontró la clave del torneo",
                data=None
            )

        return BaseResponse(
            respuesta="OK",
            mensaje="",
            data= cuenta.dict()
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