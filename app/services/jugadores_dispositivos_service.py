from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models import UsuarioDispositivos


class JugadoresDispositivosService:
    @staticmethod
    def exist_device_register(
        db: Session,
        token_firebase: str,
        usuario_id: int,
    ) -> Optional[UsuarioDispositivos]:
        return (
            db.query(UsuarioDispositivos)
            .filter(
                UsuarioDispositivos.token == token_firebase,
                UsuarioDispositivos.usuarioID == usuario_id,
            )
            .first()
        )

    @staticmethod
    def register_device_user(db: Session, token_firebase: str, user_id: int) -> None:
        try:
            existe = JugadoresDispositivosService.exist_device_register(
                db=db,
                token_firebase=token_firebase,
                usuario_id=user_id,
            )

            if existe is None:
                item = UsuarioDispositivos(
                    token=token_firebase,
                    usuarioID=user_id,
                    fechaRegistro=datetime.utcnow(),
                )
                db.add(item)
                db.commit()
                db.refresh(item)
        except Exception:
            # Mantiene el comportamiento de C#: si falla, no interrumpe otros procesos.
            db.rollback()

    @staticmethod
    def guardar_dispositivo_jugador(db: Session, jugador_id: int, dispositivo_token: str) -> None:
        # Alias para mantener compatibilidad con llamados existentes.
        JugadoresDispositivosService.register_device_user(
            db=db,
            token_firebase=dispositivo_token,
            user_id=jugador_id,
        )


# Instancia global del servicio
jugadores_dispositivos_service = JugadoresDispositivosService()