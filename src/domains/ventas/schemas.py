from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CatalogoItemResponse(BaseModel):
    id: int
    nombre: str
    precio_venta: float
    costo_unitario: float
    stock_minimo: float
    valor_puntos: int | None = None
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class MedioPagoResponse(BaseModel):
    id: int
    medio_pago: str

    model_config = ConfigDict(from_attributes=True)


class TicketItemCreate(BaseModel):
    id_producto: int
    cantidad: int = Field(..., gt=0)
    precio: float = Field(..., ge=0.0)


class TicketPagoCreate(BaseModel):
    id_medio_pago: int
    monto: float = Field(..., gt=0.0)


class TicketCreateRequest(BaseModel):
    turno_caja_id: int | None = None
    productos: list[TicketItemCreate] = Field(..., min_length=1)
    pagos: list[TicketPagoCreate] = Field(..., min_length=1)


class TicketItemResponse(BaseModel):
    id: int | None = None
    id_producto: int
    nombre_producto: str | None = None
    cantidad: int
    precio: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)


class TicketPagoResponse(BaseModel):
    id_medio_pago: int
    nombre_medio_pago: str | None = None
    monto: float

    model_config = ConfigDict(from_attributes=True)


class TicketResponse(BaseModel):
    id: int | None = None
    movimiento_id: int | None = None
    turno_caja_id: int
    fecha: datetime
    monto_total: float
    items: list[TicketItemResponse] = []
    pagos: list[TicketPagoResponse] = []

    model_config = ConfigDict(from_attributes=True)


class TicketAnularRequest(BaseModel):
    motivo: str | None = Field(None, max_length=200)
