from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UsuarioCliCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    dni: str = Field(..., pattern=r"^\d{7,8}$")
    email: EmailStr
    telefono: str | None = Field(None, max_length=50)
    fecha_nac: date
    rol_id: int


class UsuarioCliUpdateDatos(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str | None = Field(None, min_length=1, max_length=100)
    apellido: str | None = Field(None, min_length=1, max_length=100)
    dni: str | None = Field(None, pattern=r"^\d{7,8}$")
    email: EmailStr | None = None
    telefono: str | None = Field(None, max_length=50)
    fecha_nac: date | None = None

    @model_validator(mode="after")
    def validar_al_menos_un_campo(self):
        if not any([
            self.nombre,
            self.apellido,
            self.dni,
            self.email,
            self.telefono,
            self.fecha_nac,
        ]):
            raise ValueError(
                "Debe proporcionar al menos un campo para actualizar."
            )
        return self


class UsuarioCliUpdateRol(BaseModel):
    rol_id: int
