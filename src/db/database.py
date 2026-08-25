from datetime import datetime, date, time
from typing import Generator
from sqlalchemy import create_engine,Column, DateTime, func, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from src.core.config import settings
import math

Base = declarative_base()

db_url = settings.DATABASE_URL or ""
engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TimestampMixin:
    fecha_creacion = Column(DateTime, server_default=func.now(), index=True)
    fecha_modificacion = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), index=True
    )

def get_db() -> Generator:
    """Dependency to inject database session into request scope."""
    db = SessionLocal()
    try:
        db.execute(text("SET TIME ZONE 'America/Argentina/Buenos_Aires'"))
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def connection(
    proc_name: str,
    proc_params: dict | None,
    db: Session | None = None,
    timezone: str = 'America/Argentina/Buenos_Aires'
) -> dict:
    if db is None:
        raise Exception("La session de la base de datos no es valida")
    try:
        db.execute(text(f"SET TIME ZONE '{timezone}'"))
    except Exception as e:
        raise Exception(f"Error al configurar la zona horaria: {str(e)}")
    
    proc_params = proc_params or {}

    def convert_fila_a_dict(rows, colum_names):
        """Convierte una fila de SQLAlchemy a un diccionario."""
        try: 
            dict_filas = []
            cantidad_paginas = None

            for row in rows:
                row_dict = {}
                
                for index, column in enumerate(colum_names):
                    value = row[index]
                    
                    if column == "total_registros" and cantidad_paginas is None and proc_params.get("cantidad_filas"):
                        cantidad__paginas = math.ceil(
                            value / proc_params["cantidad_filas"]
                        )
                        continue
                    
                    if isinstance(value,list):
                        value = [v for v in value]
                    elif isinstance(value, datetime):
                        value = value.strftime("%d/%m/%Y %H:%M:%S")
                    elif isinstance(value, date): 
                        value = value.strftime("%d/%m/%Y")
                    elif isinstance(value, time):
                        value = value.strftime("%H:%M:%S")
                    
                    row_dict[column] = value
                
                dict_filas.append(row_dict)
            
            return dict_filas, cantidad_paginas
        
        except Exception as e:
            raise Exception(f"Error al convertir fila a diccionario: {str(e)}")

    try:
        if proc_params:
            if proc_params.get("pagina"):
                proc_params["cantidad_skip"] = (proc_params["pagina"] - 1) * proc_params["cantidad_filas"]
                del proc_params["pagina"]
            named_args = ", ".join(f"{k} := :{k}" for k in proc_params.keys())
            query = f"SELECT * FROM {proc_name}({named_args})"
            result = db.execute(text(query), proc_params)
        else:
            query = f"SELECT * FROM {proc_name}()"
            result = db.execute(text(query))
        
        rows = result.fetchall()
        column_names = result.keys()

        if len(rows) > 0:
            dict_rows, cantidad_paginas = convert_fila_a_dict(rows, column_names)
            return {
                "rows": dict_rows,
                "cantidad_paginas": cantidad_paginas,
            }
        else:
            return {"rows": [], "cantidad_paginas": None}


    except Exception as e:
        db.rollback()
        raise Exception(f"Error al obtener datos: {str(e)}")
            
