from sqlalchemy.orm import Session
from src.db.database import connection


class UsuariosCLIService:
    def __init__(self, db: Session):
        self.db = db

    def get_usuarios_cli(self) -> dict:
        response = connection('sp_get_usuarios_cli', {}, db=self.db)
        return response

    def crear_usuario_cli(self, datos: dict) -> dict:
        params = {
            'p_nombre': datos.get('nombre'),
            'p_apellido': datos.get('apellido'),
            'p_dni': datos.get('dni'),
            'p_email': datos.get('email'),
            'p_telefono': datos.get('telefono'),
            'p_fecha_nac': str(datos.get('fecha_nac')) if datos.get('fecha_nac') else None,
            'p_rol_cli_id': datos.get('rol_id'),
        }
        response = connection('sp_crear_usuario_cli', params, db=self.db)
        return response

    def actualizar_usuario_cli(self, usuario_id: int, datos: dict) -> dict:
        params = {
            'p_id': usuario_id,
            'p_nombre': datos.get('nombre'),
            'p_apellido': datos.get('apellido'),
            'p_dni': datos.get('dni'),
            'p_email': datos.get('email'),
            'p_telefono': datos.get('telefono'),
            'p_fecha_nac': str(datos.get('fecha_nac')) if datos.get('fecha_nac') else None,
        }
        response = connection('sp_actualizar_datos_usuario_cli', params, db=self.db)
        return response

    def actualizar_rol_usuario_cli(self, usuario_id: int, rol_id: int) -> dict:
        params = {
            'p_id': usuario_id,
            'p_rol_id': rol_id,
        }
        response = connection('sp_actualizar_rol_usuario_cli', params, db=self.db)
        return response

    def cambiar_estado_usuario_cli(self, usuario_id: int, estado: bool) -> dict:
        params = {
            'p_id': usuario_id,
            'p_estado': estado,
        }
        response = connection('sp_cambiar_estado_usuario_cli', params, db=self.db)
        return response