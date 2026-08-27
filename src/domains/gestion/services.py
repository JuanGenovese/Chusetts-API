from sqlalchemy.orm import Session
from src.db.database import connection

class GastosService:
    def __init__(self, db: Session):
        self.db = db

    def cargar_gasto(self, gasto_data: dict) -> dict:
        params = {
            'p_concepto': gasto_data.get('concepto'),
            'p_monto': gasto_data.get('monto'),
            'p_periodo_id': gasto_data.get('periodo_id')
        }
        return connection('sp_cargar_gasto', params, db=self.db)