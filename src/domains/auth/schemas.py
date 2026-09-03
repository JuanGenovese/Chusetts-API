from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

class LoginRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    dni: str = Field(..., pattern=r"^\d{7,8}$", description="DNI del usuario como credencial única")
    password: str = Field(..., min_length=4, max_length=74, description="Contraseña en texto plano")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CuentaAuthCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    dni: str = Field(..., pattern=r"^\d{7,8}$")
    password: str = Field(..., min_length=4)
    tipo_usuario: Literal["ADM", "CLI"]
    usuario_adm_id: int | None = None
    usuario_cli_id: int | None = None

class CuentaAuthResponse(BaseModel):
    id: int
    dni: str
    tipo_usuario: str
    activo: bool
    usuario_adm_id: int | None = None
    usuario_cli_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
    
class CuentaAuthDB(CuentaAuthCreate):
    id: int
    activo: bool
