from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.domains.auth.schemas import (
    LoginRequest, 
    TokenResponse, 
    CuentaAuthCreate, 
    CuentaAuthResponse
)
from src.domains.auth.services import (
    autenticar_usuario, 
    crear_cuenta_auth, 
)
from src.core.security import generar_token_acceso
from src.core.dependencies import obtener_cuenta_actual
from src.db.modelos.auth import CuentaAuth


router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión con DNI y contraseña")
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    """
    Inicia sesión verificando el DNI y la contraseña contra el esquema aislada `auth`.
    Devuelve un token de acceso JWT.
    """
    try:
        cuenta = autenticar_usuario(db, dni=datos.dni, password=datos.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    extra_claims = {
        "tipo_usuario": cuenta.tipo_usuario,
        "usuario_adm_id": cuenta.usuario_adm_id,
        "usuario_cli_id": cuenta.usuario_cli_id
    }
    access_token = generar_token_acceso(subject=str(cuenta.dni), info_extra=extra_claims)
    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=CuentaAuthResponse, status_code=status.HTTP_201_CREATED, summary="Registrar credenciales para un usuario")
def register_auth_account(datos: CuentaAuthCreate, db: Session = Depends(get_db)):
    """
    Crea un registro de credenciales en el esquema `auth` vinculado a un usuario en el esquema `public`.
    """
    try:
        nueva_cuenta = crear_cuenta_auth(db, datos)
        return nueva_cuenta
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/me", response_model=CuentaAuthResponse, summary="Obtener cuenta autenticada actual")
def get_me(cuenta_actual: CuentaAuth = Depends(obtener_cuenta_actual)):
    """
    Retorna la información de la cuenta autenticada según el token JWT provisto.
    """
    return cuenta_actual

