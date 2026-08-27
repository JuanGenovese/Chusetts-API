from pydantic import BaseModel
from typing import Literal


class UsuarioAdmCreate(BaseModel):
    nombre: str
    apellido: str
    dni: str
    rol_id: int

class UsuarioAdmUpdateDatos(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    dni: str | None = None

class UsuarioAdmUpdateRol(BaseModel):
    rol_id: Literal[0, 1, 2]
