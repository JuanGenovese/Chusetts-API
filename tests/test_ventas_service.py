import unittest
from unittest.mock import MagicMock
from datetime import datetime

import src.db.models
from src.domains.ventas.services import VentasService
from src.domains.ventas.schemas import (
    TicketCreateRequest,
    TicketItemCreate,
    TicketPagoCreate
)
from src.db.modelos.ventas import Productos, TurnosCaja
from src.db.modelos.gestion import MovimientosVentas, MediosPago, TiposMovimientos


class TestVentasService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.service = VentasService(self.mock_db)

    def test_crear_ticket_monto_mismatch(self):
        # 1 producto a $1000, pero pago por $800
        request = TicketCreateRequest(
            turno_caja_id=1,
            productos=[TicketItemCreate(id_producto=1, cantidad=1, precio=1000.0)],
            pagos=[TicketPagoCreate(id_medio_pago=1, monto=800.0)]
        )

        # Mock turno abierto
        self.mock_db.query().filter().first.return_value = TurnosCaja(id=1, fecha_hasta=None)

        with self.assertRaises(ValueError) as ctx:
            self.service.crear_ticket(usuario_id=1, datos=request)
        self.assertIn("no coincide", str(ctx.exception))

    def test_crear_ticket_sin_turno_falla(self):
        request = TicketCreateRequest(
            turno_caja_id=None,
            productos=[TicketItemCreate(id_producto=1, cantidad=1, precio=500.0)],
            pagos=[TicketPagoCreate(id_medio_pago=1, monto=500.0)]
        )
        # Sin turno activo
        self.mock_db.query().filter().first.return_value = None

        with self.assertRaises(ValueError) as ctx:
            self.service.crear_ticket(usuario_id=1, datos=request)
        self.assertIn("sin un turno de caja abierto", str(ctx.exception))

    def test_crear_ticket_exitoso(self):
        request = TicketCreateRequest(
            turno_caja_id=1,
            productos=[TicketItemCreate(id_producto=10, cantidad=2, precio=1500.0)],
            pagos=[TicketPagoCreate(id_medio_pago=1, monto=3000.0)]
        )

        turno = TurnosCaja(id=1, fecha_hasta=None)
        prod = Productos(id=10, nombre="Pinta IPA", precio_venta=1500.0, costo_unitario=600.0, stock_minimo=10.0, activo=True)
        medio = MediosPago(id=1, medio_pago="Efectivo")
        tipo_mov = TiposMovimientos(id=1, tipo="Venta")

        def query_side_effect(model):
            mock_q = MagicMock()
            if model == TurnosCaja:
                mock_q.filter().first.return_value = turno
            elif model == Productos:
                mock_q.filter().first.return_value = prod
            elif model == MediosPago:
                mock_q.filter().first.return_value = medio
            elif model == TiposMovimientos:
                mock_q.filter().first.return_value = tipo_mov
            else:
                mock_q.filter().first.return_value = None
                mock_q.filter().all.return_value = []
            return mock_q

        self.mock_db.query.side_effect = query_side_effect

        ticket = self.service.crear_ticket(usuario_id=1, datos=request)

        self.assertEqual(ticket.monto_total, 3000.0)
        self.assertEqual(len(ticket.items), 1)
        self.assertEqual(ticket.items[0].nombre_producto, "Pinta IPA")
        self.assertEqual(len(ticket.pagos), 1)
        self.mock_db.commit.assert_called_once()

    def test_anular_ticket_inexistente(self):
        self.mock_db.query().filter().first.return_value = None
        with self.assertRaises(ValueError) as ctx:
            self.service.anular_ticket(ticket_id=999)
        self.assertIn("No se encontró el ticket", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
