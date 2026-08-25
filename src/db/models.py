from src.db.database import Base
from src.domains.auth.models import RoleAdm, RoleCli, UsuarioAdm, UsuarioCli
from src.domains.inventario.models import (
    Stock,
    StockXMovimiento,
    ProductoComposicion,
    Proveedor,
    StockXProveedor,
)
from src.domains.caja.models import TurnoCaja
from src.domains.gestion.models import (
    TiposMovimientos,
    Movimiento,
    MovimientoVentas,
    MovimientoCompra,
    MovimientoGasto,
    MediosPagoxMovimiento,
    MedioPago,
)
from src.domains.ventas.models import (
    Producto,
    ProductoXMovimiento,
    Cupon,
    CuponUsuario,
    Punto,
)

__all__ = [
    "Base",
    "RoleAdm",
    "RoleCli",
    "UsuarioAdm",
    "UsuarioCli",
    "Stock",
    "StockXMovimiento",
    "ProductoComposicion",
    "Proveedor",
    "StockXProveedor",
    "TurnoCaja",
    "TiposMovimientos",
    "Movimiento",
    "MovimientoVentas",
    "MovimientoCompra",
    "MovimientoGasto",
    "MediosPagoxMovimiento",
    "MedioPago",
    "Producto",
    "ProductoXMovimiento",
    "Cupon",
    "CuponUsuario",
    "Punto",
]
