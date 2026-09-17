import unittest

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
            id=int(usuario.id),  # type: ignore
            nombre=str(usuario.nombre),  # type: ignore
            apellido=str(usuario.apellido),  # type: ignore
            dni=str(usuario.dni),  # type: ignore
            email=str(usuario.email),  # type: ignore
            telefono=str(usuario.telefono),  # type: ignore
            rol_id=int(usuario.rol_id),  # type: ignore
            rol=str(usuario.role.rol),  # type: ignore
            activo=bool(usuario.activo)  # type: ignore
        )

        self.assertEqual(response.id, 5)
        self.assertEqual(response.nombre, "Juan")
        self.assertEqual(response.dni, "40123456")
        self.assertEqual(response.rol, "cajero")
        self.assertTrue(response.activo)


if __name__ == "__main__":
    unittest.main()
