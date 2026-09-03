from typing import Callable
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.security import decodificar_token_acceso
from src.db.database import get_db
from src.db.modelos.auth import CuentaAuth
from src.domains.auth.services import obtener_cuenta_por_dni

# Esquema de seguridad Bearer Token (auto_error=False para manejar respuestas personalizadas)
security_scheme = HTTPBearer(auto_error=False)

# Rutas públicas exentas de autenticación global (Puerta 2 Whitelist)
PUBLIC_ROUTES: set[str] = {
    f"{settings.API_V1_STR}/auth/login",
    f"{settings.API_V1_STR}/auth/register",
    "/api/health",
    "/docs",
    "/redoc",
    "/openapi.json",
}


def es_ruta_publica(path: str) -> bool:
    """Verifica si la ruta solicitada pertenece a la lista blanca de rutas públicas."""
    if path in PUBLIC_ROUTES:
        return True
    if path.startswith("/docs") or path.startswith("/redoc"):
        return True
    return False


def verificar_autenticacion_global(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> CuentaAuth | None:
    """
    Puerta 2: Autenticación Global (Default-Deny).
    Valida el JWT Bearer para todos los endpoints privados del sistema.
    Si la ruta es pública, omite la validación.
    """
    if es_ruta_publica(request.url.path):
        return None

    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionaron credenciales de autenticación.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        payload = decodificar_token_acceso(token)
        dni = payload.sub
        if not dni:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token no contiene la identificación de usuario válida.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    cuenta = obtener_cuenta_por_dni(db, dni)
    if cuenta is None or not cuenta.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cuenta de usuario no encontrada o inactiva.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Inyectar la cuenta autenticada en el estado del request
    request.state.cuenta_actual = cuenta
    return cuenta


def obtener_cuenta_actual(request: Request) -> CuentaAuth:
    """Obtiene la cuenta autenticada almacenada en la request por la Puerta 2."""
    cuenta = getattr(request.state, "cuenta_actual", None)
    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No hay una cuenta de usuario autenticada en esta sesión.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return cuenta


def requerir_roles(*roles_permitidos: str) -> Callable[..., CuentaAuth]:
    """
    Puerta 3: Autorización por Roles (RBAC).
    Verifica que el usuario autenticado tenga uno de los roles autorizados.
    """
    def verificador_rol(cuenta: CuentaAuth = Depends(obtener_cuenta_actual)) -> CuentaAuth:
        if cuenta.tipo_usuario not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere uno de los siguientes roles: {list(roles_permitidos)}"
            )
        return cuenta

    return verificador_rol
