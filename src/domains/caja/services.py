from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.db.modelos.ventas import TurnosCaja
from src.db.modelos.gestion import MovimientosVentas, MediosPagoxMovimientos, MediosPago
from src.domains.caja.schemas import TurnoAperturaRequest, TurnoCierreRequest, TurnoResponse, ArqueoCierreResponse


class CajaService:
    def __init__(self, db: Session):
        self.db = db

    def obtener_turno_activo(self, usuario_id: int) -> TurnosCaja | None:
        return (
            self.db.query(TurnosCaja)
            .filter(TurnosCaja.usuario_id == usuario_id, TurnosCaja.fecha_hasta.is_(None))
            .first()
        )

    def abrir_turno(self, usuario_id: int, datos: TurnoAperturaRequest) -> TurnosCaja:
        turno_existente = self.obtener_turno_activo(usuario_id)
        if turno_existente:
            raise ValueError(f"El usuario ya posee un turno abierto (Turno #{turno_existente.id}). Debe cerrarlo primero.")

        nuevo_turno = TurnosCaja(
            usuario_id=usuario_id,
            fecha_desde=datetime.now(),
            fecha_hasta=None,
            efectivo_inicial=datos.efectivo_inicial,
            observacion_apertura=datos.observacion_apertura,
            observacion_cierre=None
        )
        self.db.add(nuevo_turno)
        self.db.commit()
        self.db.refresh(nuevo_turno)
        return nuevo_turno

    def cerrar_turno(self, usuario_id: int, datos: TurnoCierreRequest) -> ArqueoCierreResponse:
        turno = self.obtener_turno_activo(usuario_id)
        if not turno:
            raise ValueError("No se encontró ningún turno activo para este usuario.")

        # Calcular ventas asociadas al turno
        ventas_turno = (
            self.db.query(MovimientosVentas)
            .filter(MovimientosVentas.turno_caja_id == turno.id)
            .all()
        )

        ventas_totales = sum(v.monto_total for v in ventas_turno) if ventas_turno else 0.0

        # Desglose por medios de pago
        ventas_efectivo = 0.0
        ventas_otros = 0.0

        if ventas_turno:
            movimiento_ids = [v.movimiento_id for v in ventas_turno]
            pagos = (
                self.db.query(MediosPagoxMovimientos, MediosPago)
                .join(MediosPago, MediosPagoxMovimientos.id_medio_pago == MediosPago.id)
                .filter(MediosPagoxMovimientos.id_movimiento.in_(movimiento_ids))
                .all()
            )
            for pago, medio in pagos:
                nombre_medio = (medio.medio_pago or "").strip().lower()
                if "efectivo" in nombre_medio:
                    ventas_efectivo += pago.monto
                else:
                    ventas_otros += pago.monto

        efectivo_esperado = turno.efectivo_inicial + ventas_efectivo
        diferencia = (datos.efectivo_real - efectivo_esperado) if datos.efectivo_real is not None else None

        # Cerrar el turno
        turno.fecha_hasta = datetime.now()
        turno.observacion_cierre = datos.observacion_cierre
        self.db.commit()
        self.db.refresh(turno)

        turno_dict = {
            "id": turno.id,
            "usuario_id": turno.usuario_id,
            "fecha_desde": turno.fecha_desde,
            "fecha_hasta": turno.fecha_hasta,
            "efectivo_inicial": turno.efectivo_inicial,
            "observacion_apertura": turno.observacion_apertura,
            "observacion_cierre": turno.observacion_cierre,
            "activo": turno.fecha_hasta is None
        }

        return ArqueoCierreResponse(
            turno=TurnoResponse(**turno_dict),
            ventas_totales=ventas_totales,
            ventas_efectivo=ventas_efectivo,
            ventas_otros_medios=ventas_otros,
            efectivo_esperado=efectivo_esperado,
            efectivo_real=datos.efectivo_real,
            diferencia_efectivo=diferencia
        )

    def listar_turnos(self, limite: int = 20) -> list[TurnosCaja]:
        return (
            self.db.query(TurnosCaja)
            .order_by(TurnosCaja.id.desc())
            .limit(limite)
            .all()
        )
