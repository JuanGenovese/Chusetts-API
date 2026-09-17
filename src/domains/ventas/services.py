from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from src.db.modelos.ventas import Productos, ProductoXMovimiento, TurnosCaja
from src.db.modelos.gestion import (
    Movimientos,
    MovimientosVentas,
    TiposMovimientos,
    MediosPago,
    MediosPagoxMovimientos
)
from src.db.modelos.compras import ProductoComposicion, Stock
from src.domains.ventas.schemas import (
    TicketCreateRequest,
    TicketResponse,
    TicketItemResponse,
    TicketPagoResponse,
    CatalogoItemResponse,
    MedioPagoResponse
)


class VentasService:
    def __init__(self, db: Session):
        self.db = db

    def obtener_catalogo(self) -> list[Productos]:
        return (
            self.db.query(Productos)
            .filter(Productos.activo.is_(True))
            .order_by(Productos.nombre.asc())
            .all()
        )

    def obtener_medios_pago(self) -> list[MediosPago]:
        return (
            self.db.query(MediosPago)
            .order_by(MediosPago.id.asc())
            .all()
        )

    def _obtener_o_crear_tipo_movimiento(self, nombre: str) -> TiposMovimientos:
        tipo = self.db.query(TiposMovimientos).filter(TiposMovimientos.tipo.ilike(nombre)).first()
        if not tipo:
            tipo = TiposMovimientos(tipo=nombre)
            self.db.add(tipo)
            self.db.flush()
        return tipo

    def crear_ticket(self, usuario_id: int, datos: TicketCreateRequest) -> TicketResponse:
        # 1. Determinar y validar turno de caja
        turno_id = datos.turno_caja_id
        if not turno_id:
            turno_activo = (
                self.db.query(TurnosCaja)
                .filter(TurnosCaja.usuario_id == usuario_id, TurnosCaja.fecha_hasta.is_(None))
                .first()
            )
            if not turno_activo:
                raise ValueError("No se puede emitir una venta sin un turno de caja abierto para el usuario.")
            turno_id = turno_activo.id
        else:
            turno = self.db.query(TurnosCaja).filter(TurnosCaja.id == turno_id).first()
            if not turno or turno.fecha_hasta is not None:
                raise ValueError(f"El turno #{turno_id} no existe o ya se encuentra cerrado.")

        # 2. Validar coherencia de montos
        total_productos = sum(item.cantidad * item.precio for item in datos.productos)
        total_pagos = sum(pago.monto for pago in datos.pagos)
        if round(total_productos, 2) != round(total_pagos, 2):
            raise ValueError(
                f"El monto total de los medios de pago (${round(total_pagos, 2)}) "
                f"no coincide con el total de los productos (${round(total_productos, 2)})."
            )

        # 3. Crear Movimiento general de Venta
        tipo_venta = self._obtener_o_crear_tipo_movimiento("Venta")
        ahora = datetime.now()

        movimiento = Movimientos(
            tipo_id=tipo_venta.id,
            fecha=ahora
        )
        self.db.add(movimiento)
        self.db.flush()

        # 4. Crear Movimiento de Venta
        mov_venta = MovimientosVentas(
            movimiento_id=movimiento.id,
            turno_caja_id=turno_id,
            monto_total=total_productos,
            fecha=ahora
        )
        self.db.add(mov_venta)
        self.db.flush()

        # 5. Registrar productos e impactar stock
        items_response: list[TicketItemResponse] = []
        for item in datos.productos:
            prod = self.db.query(Productos).filter(Productos.id == item.id_producto).first()
            if not prod:
                raise ValueError(f"Producto con ID {item.id_producto} no encontrado.")

            pxm = ProductoXMovimiento(
                id_movimiento_venta=mov_venta.id,
                id_producto=item.id_producto,
                cantidad_producto=item.cantidad,
                precio=item.precio
            )
            self.db.add(pxm)
            self.db.flush()

            # Descontar stock si tiene composición
            composiciones = (
                self.db.query(ProductoComposicion)
                .filter(ProductoComposicion.id_producto == prod.id)
                .all()
            )
            for comp in composiciones:
                stock_item = self.db.query(Stock).filter(Stock.id == comp.id_stock).first()
                if stock_item:
                    stock_item.cantidad -= (comp.cantidad_usada * item.cantidad)

            items_response.append(
                TicketItemResponse(
                    id=pxm.id,
                    id_producto=item.id_producto,
                    nombre_producto=prod.nombre,
                    cantidad=item.cantidad,
                    precio=item.precio,
                    subtotal=round(item.cantidad * item.precio, 2)
                )
            )

        # 6. Registrar pagos
        pagos_response: list[TicketPagoResponse] = []
        for pago in datos.pagos:
            medio = self.db.query(MediosPago).filter(MediosPago.id == pago.id_medio_pago).first()
            if not medio:
                raise ValueError(f"Medio de pago con ID {pago.id_medio_pago} no encontrado.")

            mxp = MediosPagoxMovimientos(
                id_movimiento=movimiento.id,
                id_medio_pago=pago.id_medio_pago,
                monto=pago.monto
            )
            self.db.add(mxp)

            pagos_response.append(
                TicketPagoResponse(
                    id_medio_pago=pago.id_medio_pago,
                    nombre_medio_pago=medio.medio_pago,
                    monto=pago.monto
                )
            )

        self.db.commit()

        return TicketResponse(
            id=mov_venta.id,
            movimiento_id=movimiento.id,
            turno_caja_id=turno_id,
            fecha=ahora,
            monto_total=total_productos,
            items=items_response,
            pagos=pagos_response
        )

    def listar_tickets(self, turno_caja_id: int | None = None, limite: int = 50) -> list[TicketResponse]:
        query = self.db.query(MovimientosVentas)
        if turno_caja_id is not None:
            query = query.filter(MovimientosVentas.turno_caja_id == turno_caja_id)

        ventas = query.order_by(MovimientosVentas.id.desc()).limit(limite).all()

        resultado: list[TicketResponse] = []
        for v in ventas:
            # Recuperar items
            items = (
                self.db.query(ProductoXMovimiento, Productos)
                .join(Productos, ProductoXMovimiento.id_producto == Productos.id)
                .filter(ProductoXMovimiento.id_movimiento_venta == v.id)
                .all()
            )
            items_res = [
                TicketItemResponse(
                    id=pxm.id,
                    id_producto=pxm.id_producto,
                    nombre_producto=p.nombre,
                    cantidad=pxm.cantidad_producto,
                    precio=pxm.precio,
                    subtotal=round(pxm.cantidad_producto * pxm.precio, 2)
                )
                for pxm, p in items
            ]

            # Recuperar pagos
            pagos = (
                self.db.query(MediosPagoxMovimientos, MediosPago)
                .join(MediosPago, MediosPagoxMovimientos.id_medio_pago == MediosPago.id)
                .filter(MediosPagoxMovimientos.id_movimiento == v.movimiento_id)
                .all()
            )
            pagos_res = [
                TicketPagoResponse(
                    id_medio_pago=mxp.id_medio_pago,
                    nombre_medio_pago=mp.medio_pago,
                    monto=mxp.monto
                )
                for mxp, mp in pagos
            ]

            resultado.append(
                TicketResponse(
                    id=v.id,
                    movimiento_id=v.movimiento_id,
                    turno_caja_id=v.turno_caja_id,
                    fecha=v.fecha,
                    monto_total=v.monto_total,
                    items=items_res,
                    pagos=pagos_res
                )
            )

        return resultado

    def anular_ticket(self, ticket_id: int, motivo: str | None = None) -> dict:
        venta = self.db.query(MovimientosVentas).filter(MovimientosVentas.id == ticket_id).first()
        if not venta:
            raise ValueError(f"No se encontró el ticket #{ticket_id}.")

        # Revertir stock de composiciones
        pxm_items = (
            self.db.query(ProductoXMovimiento)
            .filter(ProductoXMovimiento.id_movimiento_venta == venta.id)
            .all()
        )
        for pxm in pxm_items:
            composiciones = (
                self.db.query(ProductoComposicion)
                .filter(ProductoComposicion.id_producto == pxm.id_producto)
                .all()
            )
            for comp in composiciones:
                stock_item = self.db.query(Stock).filter(Stock.id == comp.id_stock).first()
                if stock_item:
                    stock_item.cantidad += (comp.cantidad_usada * pxm.cantidad_producto)

        # Actualizar tipo de movimiento a Anulación si existe
        mov = self.db.query(Movimientos).filter(Movimientos.id == venta.movimiento_id).first()
        if mov:
            tipo_anulacion = self._obtener_o_crear_tipo_movimiento("Anulacion Venta")
            mov.tipo_id = tipo_anulacion.id

        self.db.commit()
        return {
            "message": f"Ticket #{ticket_id} anulado exitosamente",
            "ticket_id": ticket_id,
            "motivo": motivo
        }
