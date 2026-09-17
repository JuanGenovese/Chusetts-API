from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TurnoAperturaRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    efectivo_inicial: float = Field(0.0, ge=0.0)
    observacion_apertura: str = Field(..., min_length=1, max_length=100)


class TurnoCierreRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    observacion_cierre: str | None = Field(None, max_length=100)
    efectivo_real: float | None = Field(None, ge=0.0)


class TurnoResponse(BaseModel):
    id: int
    usuario_id: int
    fecha_desde: datetime
    fecha_hasta: datetime | None = None
    efectivo_inicial: float
    observacion_apertura: str
    observacion_cierre: str | None = None
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class ArqueoCierreResponse(BaseModel):
    turno: TurnoResponse
    ventas_totales: float
    ventas_efectivo: float
    ventas_otros_medios: float
    efectivo_esperado: float
    efectivo_real: float | None = None
    diferencia_efectivo: float | None = None
