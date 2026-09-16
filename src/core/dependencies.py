from typing import Callable
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.security import decodificar_token_acceso
from src.db.database import get_db
from src.db.modelos.auth import CuentaAuth
from src.domains.auth.services import AuthService
from src.db.modelos.usuarios import Usuarios

security_scheme = HTTPBearer(auto_error=False)

PUBLIC_ROUTES: set[str] = {
    f"{settings.API_V1_STR}/auth/login",
    f"{settings.API_V1_STR}/auth/register",
    "/api/health",
    "/openapi.json"
}


def es_ruta_publica(path: str) -> bool:
    """Verifica si la ruta pertenece a la lista de rutas que no necesitan autenticación."""
    return path in PUBLIC_ROUTES or path.startswith("/docs") or path.startswith("/redoc")


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

    cuenta = AuthService(db).obtener_cuenta_por_dni(dni)
    if cuenta is None or not cuenta.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cuenta de usuario no encontrada o inactiva.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    usuario = db.query(Usuarios).filter(Usuarios.cuenta_id == cuenta.id).first()

    # Inyectar la cuenta autenticada en el estado del request
    request.state.usuario_actual = usuario
    return usuario


def obtener_usuario_actual(request: Request) -> Usuarios:
    """Obtiene la cuenta autenticada almacenada en la request por la Puerta 2."""
    usuario = getattr(request.state, "usuario_actual", None)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No hay una cuenta de usuario autenticada en esta sesión.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usuario


def requerir_roles(*roles_permitidos: int) -> Callable[..., Usuarios]:
    """
    Puerta 3: Autorización por Roles (RBAC).
    Verifica que el usuario autenticado tenga uno de los roles autorizados.
    """
    def verificador_rol(usuario: Usuarios = Depends(obtener_usuario_actual)) -> Usuarios:
        if usuario.rol_id is not 0 and usuario.rol_id not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere uno de los siguientes roles: {list(roles_permitidos)}"
            )
        return usuario

    return verificador_rol
