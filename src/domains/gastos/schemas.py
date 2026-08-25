from pydantic import BaseModel
from typing import Optional

class GastosCreate(BaseModel):
    concepto: str
    monto: float
    periodo_id: int
    