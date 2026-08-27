from sqlalchemy.orm import Session
from src.db.database import connection

class UsuariosCLIService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_usuarios_cli(self) -> dict:
        response = connection('sp_get_usuarios_cli', {}, db=self.db)
        return response