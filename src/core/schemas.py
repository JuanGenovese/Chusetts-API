from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: str
    exp: int
    tipo_usuario: str | None = None
    usuario_adm_id: int | None = None
    usuario_cli_id: int | None = None
    