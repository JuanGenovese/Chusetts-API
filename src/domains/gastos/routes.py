from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.domains.gastos.services import GastosService
from src.domains.gastos.schemas import GastosCreate

router = APIRouter(prefix="/gastos", tags=["Gastos  Varios"])


@router.post("/cargar_gasto", status_code=status.HTTP_201_CREATED)
def cargar_gasto(
    gasto_data: GastosCreate,
    db: Session = Depends(get_db)
):
    try:
        service = GastosService(db)
        response = service.cargar_gasto(gasto_data.model_dump())

        rows = response.get("rows", [])
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo cargar el gasto"
            )

        return {
            "message": "Gasto cargado exitosamente",
            "data": rows[0]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )