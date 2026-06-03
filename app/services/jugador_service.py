from typing import Optional

from sqlalchemy.orm import Session
from app.models import Jugador
from app.schemas import JugadorSchema, LoginJugadorRequest, UsuarioResponse
from app.auth import generate_jwt_token
from app.utils.image_utils import save_image_base64
from app.services.jugadores_dispositivos_service import jugadores_dispositivos_service
Cyan = "\033[36m"

class JugadorService:
    #Metodo para crear un jugador o actualizarlo si ya existe,
    #Para que un jugador se cree, es necesario que el correo no exista previamente en la base de datos,
    #si el correo ya existe, se actualizan los datos del jugador existente con los datos 
    #recibe un JugadorSchema con los datos del jugador a crear o actualizar, 
    #y devuelve un UsuarioResponse con los datos del jugador creado o actualizado, 
    #incluyendo un token JWT para autenticación en la app. 
    #Si ocurre un error, lanza una excepción con el mensaje de error.
    @staticmethod
    def crear_jugador(db: Session, jugador_data: JugadorSchema) -> UsuarioResponse:
        data_jugador = {}

        if jugador_data.nombre is not None:
            data_jugador["nombre"] = jugador_data.nombre
        if jugador_data.apellido is not None:
            data_jugador["apellido"] = jugador_data.apellido
        if jugador_data.email is not None:
            data_jugador["email"] = jugador_data.email
        if jugador_data.contrasenia is not None:
            data_jugador["contrasenia"] = jugador_data.contrasenia
        if jugador_data.origen is not None:
            data_jugador["origen"] = jugador_data.origen
        if jugador_data.fechaNacimiento is not None:
            data_jugador["fechaNacimiento"] = jugador_data.fechaNacimiento
        if jugador_data.talla is not None:
            data_jugador["talla"] = jugador_data.talla
        if jugador_data.noJugador is not None:
            data_jugador["noJugador"] = jugador_data.noJugador
        if jugador_data.nombreJersy is not None:
            data_jugador["nombreJersy"] = jugador_data.nombreJersy
        if jugador_data.codigoPostal is not None:
            data_jugador["codigoPostal"] = jugador_data.codigoPostal
        if jugador_data.categoriaID is not None:
            data_jugador["categoriaID"] = jugador_data.categoriaID
        if jugador_data.telefono is not None:
            data_jugador["telefono"] = jugador_data.telefono
        if jugador_data.tipoDeporte is not None:
            data_jugador["tipoDeporte"] = jugador_data.tipoDeporte

        # Insert o update según correo.
        nuevo_jugador = None
        correo = (jugador_data.email or "").strip()
        if correo:
            nuevo_jugador = db.query(Jugador).filter(Jugador.email == correo).first()

        # Si viene foto en base64, se procesa después de saber si es alta o update.
        foto_guardada = None
        if jugador_data.foto:
            id_para_foto = nuevo_jugador.id if nuevo_jugador is not None else (jugador_data.id or 0)
            foto_resultado = save_image_base64(
                base64img=jugador_data.foto,
                id_value=id_para_foto,
                texto="FotoJugador_",
                tipo="images",
            )
            if not foto_resultado.startswith("Error:"):
                foto_guardada = foto_resultado
            elif nuevo_jugador is None:
                foto_guardada = "FotoEquipo_Default.png"

        if foto_guardada is not None:
            data_jugador["foto"] = foto_guardada

        if nuevo_jugador is None:
            # Defaults para alta nueva.
            if "foto" not in data_jugador:
                data_jugador["foto"] = "FotoEquipo_Default.png"
            if "posicion" not in data_jugador:
                data_jugador["posicion"] = "Jugador"
            if "tipoDeporte" not in data_jugador:
                data_jugador["tipoDeporte"] = "PADEL"

            nuevo_jugador = Jugador(**data_jugador)
            db.add(nuevo_jugador)
        else:
            for key, value in data_jugador.items():
                setattr(nuevo_jugador, key, value)

        db.commit()
        db.refresh(nuevo_jugador)

        #Guardamos el dipositivo del jugador
        if jugador_data.tokenFirebase:
            jugadores_dispositivos_service.guardar_dispositivo_jugador(
                db=db,
                jugador_id=nuevo_jugador.id,
                dispositivo_token=jugador_data.tokenFirebase,
            )
        

        token = generate_jwt_token(
            user_id=nuevo_jugador.id,
            name=nuevo_jugador.nombre or "",
            email=nuevo_jugador.email or "",
        )

        usuario_data = {
            "id": nuevo_jugador.id,
            "nombre": nuevo_jugador.nombre,
            "apellido": nuevo_jugador.apellido,
            "correo": nuevo_jugador.email,
            "telefono": nuevo_jugador.telefono,
            "estado": nuevo_jugador.estado,
            "foto": nuevo_jugador.foto,
            "origen": nuevo_jugador.origen,
            "token": token
        }

        return UsuarioResponse(**usuario_data)
    
    #Metodo para obtener un jugador por su correo electrónico, útil para login o validaciones previas al registro
    @staticmethod
    def obtener_jugador_por_correo(db: Session, correo: str) -> Optional[Jugador]:
        try:
            query = db.query(Jugador).filter(Jugador.email == correo).first()
            return query
        except Exception as ex:
            print(f"{Cyan}Error al obtener jugador por correo: {ex}")
            return Exception(f"Error al obtener jugador por correo: {ex}")

    #Metodo para poder hacer login de un jugador, este puede hacer login por correo o numero de telefono
    @staticmethod
    def login_jugador(db: Session, login_request: LoginJugadorRequest) -> Optional[UsuarioResponse]:
        jugador = db.query(Jugador).filter(
            (Jugador.email == login_request.usuario_telefono) | (Jugador.telefono == login_request.usuario_telefono),
            Jugador.contrasenia == login_request.contrasena
        ).first()

        if jugador is None:
            return Exception("Credenciales inválidas")
        

        #Guardamos el dipositivo del jugador
        if login_request.tokenFirebase:
            jugadores_dispositivos_service.guardar_dispositivo_jugador(
                db=db,
                jugador_id=jugador.id,
                dispositivo_token=login_request.tokenFirebase,
            )
        
        token = generate_jwt_token(
            user_id=jugador.id,
            name=jugador.nombre or "",
            email=jugador.email or "",
        )

        usuario_data = {
            "id": jugador.id,
            "nombre": jugador.nombre,
            "apellido": jugador.apellido,
            "correo": jugador.email,
            "telefono": jugador.telefono,
            "estado": jugador.estado,
            "foto": jugador.foto,
            "origen": jugador.origen,
            "token": token
        }

        return UsuarioResponse(**usuario_data)  

# Instancia global del servicio
jugador_service = JugadorService()