import unittest

import src.db.models
from src.domains.auth.schemas import UsuarioMeResponse
from src.db.modelos.usuarios import Usuarios, Roles


class TestAuthMe(unittest.TestCase):
    def test_usuario_me_response_schema(self):
        rol = Roles(id=2, rol="cajero")
        usuario = Usuarios(
            id=5,
            cuenta_id=10,
            nombre="Juan",
            apellido="Pérez",
            dni="40123456",
            email="juan@cerveceria.com",
            telefono="1122334455",
            rol_id=2,
            activo=True
        )
        usuario.role = rol

        response = UsuarioMeResponse(
            id=usuario.id,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            dni=usuario.dni,
            email=usuario.email,
            telefono=usuario.telefono,
            rol_id=usuario.rol_id,
            rol=usuario.role.rol,
            activo=usuario.activo
        )

        self.assertEqual(response.id, 5)
        self.assertEqual(response.nombre, "Juan")
        self.assertEqual(response.dni, "40123456")
        self.assertEqual(response.rol, "cajero")
        self.assertTrue(response.activo)


if __name__ == "__main__":
    unittest.main()
