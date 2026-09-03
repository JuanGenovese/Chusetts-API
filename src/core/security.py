from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from src.core.config import settings
from src.core.schemas import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_contrasena(contrasena_texto_plano: str, contrasena_hasheada: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con su hash."""
    return pwd_context.verify(contrasena_texto_plano, contrasena_hasheada)

def generar_contrasena_hasheada(contrasena: str) -> str:
    """Genera el hash bcrypt de una contraseña."""
    return pwd_context.hash(contrasena)

def generar_token_acceso(
    subject: str,
    info_extra: dict | None = None
) -> str:
    """Crea un token de acceso JWT con expiration y claims opcionales."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": subject}
    if info_extra:
        to_encode.update(info_extra)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decodificar_token_acceso(token: str) -> TokenPayload:
    """Decodifica un token JWT o lanza JWTError si es inválido."""
    payload_dict = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return TokenPayload(**payload_dict)