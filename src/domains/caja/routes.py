from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.core.dependencies import obtener_usuario_actual
from src.db.modelos.usuarios import Usuarios
from src.domains.caja.schemas import (
    TurnoAperturaRequest,
    TurnoCierreRequest,
    TurnoResponse,
    ArqueoCierreResponse
)
from src.domains.caja.services import CajaService

router = APIRouter(prefix="/caja", tags=["Caja / Turnos"])


@router.get("/turno-actual", response_model=TurnoResponse | None)
def obtener_turno_actual(
    usuario: Usuarios = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Retorna el turno de caja actualmente abierto del usuario, o null si no tiene turno abierto.
    """
    service = CajaService(db)
    turno = service.obtener_turno_activo(usuario.id)
    if not turno:
        return None

    return TurnoResponse(
        id=turno.id,
        usuario_id=turno.usuario_id,
        fecha_desde=turno.fecha_desde,
        fecha_hasta=turno.fecha_hasta,
        efectivo_inicial=turno.efectivo_inicial,
        observacion_apertura=turno.observacion_apertura,
        observacion_cierre=turno.observacion_cierre,
        activo=turno.fecha_hasta is None
    )


@router.post("/abrir-turno", response_model=TurnoResponse, status_code=status.HTTP_201_CREATED)
def abrir_turno(
    datos: TurnoAperturaRequest,
    usuario: Usuarios = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Abre un nuevo turno de caja con efectivo inicial y observación de apertura.
    """
    service = CajaService(db)
    try:
        turno = service.abrir_turno(usuario.id, datos)
        return TurnoResponse(
            id=turno.id,
            usuario_id=turno.usuario_id,
            fecha_desde=turno.fecha_desde,
            fecha_hasta=turno.fecha_hasta,
            efectivo_inicial=turno.efectivo_inicial,
            observacion_apertura=turno.observacion_apertura,
            observacion_cierre=turno.observacion_cierre,
            activo=turno.fecha_hasta is None
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/cerrar-turno", response_model=ArqueoCierreResponse)
def cerrar_turno(
    datos: TurnoCierreRequest,
    usuario: Usuarios = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """
    Cierra el turno de caja activo, calculando el arqueo de ventas por medio de pago.
    """
    service = CajaService(db)
    try:
        arqueo = service.cerrar_turno(usuario.id, datos)
        return arqueo
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/turnos", response_model=list[TurnoResponse])
def listar_turnos(
    limite: int = 20,
    db: Session = Depends(get_db)
):
    """
    Lista los últimos turnos registrados.
    """
    service = CajaService(db)
    turnos = service.listar_turnos(limite=limite)
    return [
        TurnoResponse(
            id=t.id,
            usuario_id=t.usuario_id,
            fecha_desde=t.fecha_desde,
            fecha_hasta=t.fecha_hasta,
            efectivo_inicial=t.efectivo_inicial,
            observacion_apertura=t.observacion_apertura,
            observacion_cierre=t.observacion_cierre,
            activo=t.fecha_hasta is None
        )
        for t in turnos
    ]
