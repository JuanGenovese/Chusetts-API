from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.domains.auth.schemas import (
    LoginRequest, 
    TokenResponse, 
    CuentaAuthCreate, 
    CuentaAuthResponse,
    UsuarioMeResponse
)
from src.domains.auth.services import AuthService
from src.core.security import generar_token_acceso
from src.core.dependencies import obtener_usuario_actual
from src.db.modelos.usuarios import Usuarios


router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def login(
    datos: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Inicia sesión verificando el DNI y la contraseña.
    """
    try:
        service = AuthService(db)
        usuario = service.autenticar_usuario(datos.dni, datos.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    access_token = generar_token_acceso(subject=str(usuario.dni))
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=CuentaAuthResponse, status_code=status.HTTP_201_CREATED)
def register_auth_account(
    datos: CuentaAuthCreate, 
    db: Session = Depends(get_db)
):
    """
    Registra un usuario nuevo
    """
    try:
        service = AuthService(db)
        nueva_cuenta = service.crear_cuenta(datos)
        return nueva_cuenta
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/me", response_model=UsuarioMeResponse)
def get_current_user_profile(
    usuario: Usuarios = Depends(obtener_usuario_actual)
):
    """
    Retorna los datos del usuario autenticado a partir del token JWT.
    """
    return UsuarioMeResponse(
        id=usuario.id,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        dni=usuario.dni,
        email=usuario.email,
        telefono=usuario.telefono,
        rol_id=usuario.rol_id,
        rol=usuario.role.rol if usuario.role else None,
        activo=usuario.activo,
    )