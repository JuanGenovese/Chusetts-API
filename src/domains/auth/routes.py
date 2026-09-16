from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.domains.auth.schemas import (
    LoginRequest, 
    TokenResponse, 
    CuentaAuthCreate, 
    CuentaAuthResponse
)
from src.domains.auth.services import AuthService
from src.core.security import generar_token_acceso
from src.core.dependencies import obtener_cuenta_actual
from src.db.modelos.auth import CuentaAuth


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
        cuenta = service.autenticar_usuario(datos.dni, datos.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    extra_claims = {
        "tipo_usuario": cuenta.tipo_usuario,
        "usuario_adm_id": cuenta.usuario_adm_id,
        "usuario_cli_id": cuenta.usuario_cli_id
    }
    access_token = generar_token_acceso(subject=str(cuenta.dni), info_extra=extra_claims)
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


@router.get("/me", response_model=CuentaAuthResponse)
def get_me(
    cuenta_actual: CuentaAuth = Depends(obtener_cuenta_actual),
    db: Session = Depends(get_db)
):
    """
    Retorna la información de la cuenta autenticada según el token JWT provisto.
    """
    return cuenta_actual