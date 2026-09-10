from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Literal


class UsuarioAdmCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    dni: str = Field(..., pattern=r"^\d{7,8}$")
    rol_id: int


class UsuarioAdmUpdateDatos(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str | None = Field(None, min_length=1, max_length=100)
    apellido: str | None = Field(None, min_length=1, max_length=100)
    dni: str | None = Field(None, pattern=r"^\d{7,8}$")

    @model_validator(mode="after")
    def validar_al_menos_un_campo(self):
        if not any([self.nombre, self.apellido, self.dni]):
            raise ValueError("Debe proporcionar al menos un campo (nombre, apellido o DNI) para actualizar.")
        return self


class UsuarioAdmUpdateRol(BaseModel):
    rol_id: Literal[0, 1, 2]

