from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.domains.usuarios.cli.services import UsuariosCLIService

router = APIRouter(prefix="/usuarios", tags=["UsuariosCLI"])

@router.get("/cli", status_code=status.HTTP_200_OK)
def obtener_usuarios_cli(
    db: Session = Depends(get_db)
):
    """Obtiene todos los usuarios del lado de clientes"""
    try:
        service = UsuariosCLIService(db)
        response = service.get_usuarios_cli()

        rows = response.get("rows", [])
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron usuarios del lado de clientes"
            )

        return {
            "message": "Usuarios del lado de clientes obtenidos exitosamente",
            "data": rows
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )