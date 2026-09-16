from datetime import date
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

    nombre: str = Field(..., min_length=1)
    apellido: str = Field(..., min_length=1)
    dni: str = Field(..., pattern=r"^\d{7,8}$")
    email: str = Field(..., min_length=1)
    telefono: str = Field(..., min_length=1)
    fecha_nac: str = Field(..., pattern=r"^\d{2}/\d{2}/\d{4}$")
    rol_id: int
    password: str = Field(..., min_length=4)

class UsuarioCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    dni: str = Field(..., pattern=r"^\d{7,8}$")
    rol_id: int

class CuentaAuthResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    dni: str
    email: str
    telefono: str
    fecha_nac: date
    rol_id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)
    
class CuentaAuthDB(CuentaAuthCreate):
    id: int
    activo: bool
