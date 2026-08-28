from typing import Generator
from sqlalchemy import create_engine,Column, DateTime, func, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from src.core.config import settings
import math
import re

IDENTIFIER_REGEX = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)?$")

Base = declarative_base()

db_url = settings.DATABASE_URL or ""
engine = create_engine(
    db_url,
    connect_args={
        "options": "-c timezone=America/Argentina/Buenos_Aires"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TimestampMixin:
    create_at = Column(DateTime, server_default=func.now(), index=True)
    update_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), index=True)

def get_db() -> Generator[Session, None, None]:
    """Obtiene una instancia de la sesion de la base de datos."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

def connection(
    proc_name: str,
    proc_params: dict | None = None,
    db: Session | None = None
) -> dict:
    """Ejecuta un procedimiento almacenado y devuelve el resultado."""
    if db is None:
        raise ValueError("La sesión de la base de datos no es válida")
    
    if not proc_name or not proc_name.startswith("sp_"):
        raise ValueError("El procedimiento debe especificar un nombre válido que comience con 'sp_'.")
    
    if not IDENTIFIER_REGEX.match(proc_name):
        raise ValueError(f"Nombre de procedimiento inválido: '{proc_name}'")

    params = (proc_params or {}).copy()

    for key in params.keys():
        if not IDENTIFIER_REGEX.match(key):
            raise ValueError(f"Nombre de parámetro inválido: '{key}'")
    
    cantidad_filas = params.get("cantidad_filas")
    pagina = params.get("pagina")

    if pagina is not None and cantidad_filas is not None:
        if pagina < 1 or cantidad_filas < 1:
            raise ValueError("Los parámetros 'pagina' y 'cantidad_filas' deben ser mayores o iguales a 1.")
        params["cantidad_skip"] = (pagina - 1) * cantidad_filas
        del params["pagina"]

    try:
        if params:
            named_args = ", ".join(f"{k} := :{k}" for k in params.keys())
            query = text(f"SELECT * FROM {proc_name}({named_args})")
            result = db.execute(query, params)
        else:
            query = text(f"SELECT * FROM {proc_name}()")
            result = db.execute(query)

        rows = [dict(row) for row in result.mappings()]
        cantidad_paginas = None

        if rows:
            if "total_registros" in rows[0] and cantidad_filas:
                total_registros = rows[0]["total_registros"]
                cantidad_paginas = math.ceil(total_registros / cantidad_filas)

            for row in rows:
                row.pop("total_registros", None)

            return {
                "rows": rows,
                "cantidad_paginas": cantidad_paginas,
            }

        return {"rows": [], "cantidad_paginas": None}

    except Exception as e:
        db.rollback()
        orig = getattr(e, "orig", e)
        if hasattr(orig, "diag") and getattr(orig.diag, "message_primary", None):
            raise ValueError(orig.diag.message_primary) from e
            
        msg = str(e)
        match = re.search(r"RaiseException\)\s*(.*?)(?:\n|CONTEXT:|$)", msg)
        if match:
            raise ValueError(match.group(1).strip()) from e

        raise Exception(f"Error al obtener datos de {proc_name}: {str(e)}") from e
            
