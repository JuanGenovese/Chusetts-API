from sqlalchemy.orm import Session
from src.db.database import connection

class UsuariosService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_usuarios(self) -> dict:
        response = connection('sp_get_usuarios', {}, db=self.db)
        return response
     
    def crear_usuario(self, datos: dict) -> dict:
        params = {
            'p_nombre': datos.get('nombre'),
            'p_apellido': datos.get('apellido'),
            'p_dni': datos.get('dni'),
            'p_rol_id': datos.get('rol_id')
        }
        response = connection('sp_crear_usuario', params, db=self.db)
        return response
    
    def actualizar_usuario(self, usuario_id: int, datos: dict) -> dict:
        params = {
            'p_id': usuario_id,
            'p_nombre': datos.get('nombre'),
            'p_apellido': datos.get('apellido'),
            'p_dni': datos.get('dni')
        }
        response = connection('sp_actualizar_datos_usuario', params, db=self.db)
        return response
   
    def actualizar_rol_usuario(self, usuario_id: int, rol_id: int) -> dict:
        params = {
            'p_id': usuario_id,
            'p_rol_id': rol_id
        }
        response = connection('sp_actualizar_rol_usuario', params, db=self.db)
        return response

    def cambiar_estado_usuario(self, usuario_id: int, estado: bool) -> dict:
        params = {
            'p_id': usuario_id,
            'p_estado': estado
        }
        response = connection('sp_cambiar_estado_usuario', params, db=self.db)
        return response