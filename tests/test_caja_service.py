import unittest
from unittest.mock import MagicMock
from datetime import datetime

import src.db.models
from src.domains.caja.services import CajaService
from src.domains.caja.schemas import TurnoAperturaRequest, TurnoCierreRequest
from src.db.modelos.ventas import TurnosCaja


class TestCajaService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.service = CajaService(self.mock_db)

    def test_abrir_turno_exitoso(self):
        # Simular que no hay turno activo previo
        self.mock_db.query().filter().first.return_value = None

        request = TurnoAperturaRequest(
            efectivo_inicial=5000.0,
            observacion_apertura="Apertura turno mañana"
        )
        turno = self.service.abrir_turno(usuario_id=1, datos=request)

        self.assertEqual(turno.usuario_id, 1)
        self.assertEqual(turno.efectivo_inicial, 5000.0)
        self.assertEqual(turno.observacion_apertura, "Apertura turno mañana")
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()

    def test_abrir_turno_falla_si_ya_existe_activo(self):
        # Simular que ya hay un turno activo
        turno_existente = TurnosCaja(id=99, usuario_id=1, fecha_hasta=None)
        self.mock_db.query().filter().first.return_value = turno_existente

        request = TurnoAperturaRequest(
            efectivo_inicial=1000.0,
            observacion_apertura="Intento duplicado"
        )
        with self.assertRaises(ValueError) as ctx:
            self.service.abrir_turno(usuario_id=1, datos=request)
        self.assertIn("ya posee un turno abierto", str(ctx.exception))

    def test_cerrar_turno_falla_si_no_hay_activo(self):
        self.mock_db.query().filter().first.return_value = None

        request = TurnoCierreRequest(observacion_cierre="Cierre sin turno")
        with self.assertRaises(ValueError) as ctx:
            self.service.cerrar_turno(usuario_id=1, datos=request)
        self.assertIn("No se encontró ningún turno activo", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
