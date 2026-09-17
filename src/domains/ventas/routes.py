from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.core.dependencies import obtener_usuario_actual
from src.db.modelos.usuarios import Usuarios
from src.domains.ventas.schemas import (
    CatalogoItemResponse,
    MedioPagoResponse,
    TicketCreateRequest,
    TicketResponse,
    TicketAnularRequest
)
from src.domains.ventas.services import VentasService

router = APIRouter(prefix="/ventas", tags=["Ventas"])


@router.get("/catalogo", response_model=list[CatalogoItemResponse])
def listar_catalogo(
    db: Session = Depends(get_db)
):
    """
    Lista todos los productos activos disponibles para la venta en el punto de venta (POS).
    """
    service = VentasService(db)
    return service.obtener_catalogo()


@router.get("/medios-pago", response_model=list[MedioPagoResponse])
def listar_medios_pago(
    db: Session = Depends(get_db)
):
    """
    Lista todos los medios de pago configurados en el sistema.
    """
    service = VentasService(db)
    return service.obtener_medios_pago()


@router.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def emitir_ticket(
    datos: TicketCreateRequest,
    usuario: Usuarios = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Emite un nuevo ticket de venta, registrando productos, pagos, y asociándolo al turno activo.
    """
    service = VentasService(db)
    try:
        ticket = service.crear_ticket(usuario_id=usuario.id, datos=datos)
        return ticket
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/tickets", response_model=list[TicketResponse])
def listar_tickets(
    turno_id: int | None = None,
    limite: int = 50,
    db: Session = Depends(get_db)
):
    """
    Lista tickets de venta emitidos, opcionalmente filtrados por turno de caja.
    """
    service = VentasService(db)
    return service.listar_tickets(turno_caja_id=turno_id, limite=limite)


@router.post("/tickets/{ticket_id}/anular")
def anular_ticket(
    ticket_id: int,
    datos: TicketAnularRequest = TicketAnularRequest(),
    db: Session = Depends(get_db)
):
    """
    Anula un ticket de venta y restituye el stock correspondiente.
    """
    service = VentasService(db)
    try:
        resultado = service.anular_ticket(ticket_id=ticket_id, motivo=datos.motivo)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
