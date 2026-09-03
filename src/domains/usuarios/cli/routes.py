from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.core.dependencies import requerir_roles
from src.domains.usuarios.cli.schemas import (
    UsuarioCliCreate,
    UsuarioCliUpdateDatos,
    UsuarioCliUpdateRol,
)
from src.domains.usuarios.cli.services import UsuariosCLIService

router = APIRouter(
    prefix="/usuarios", 
    tags=["UsuariosCLI"],
    dependencies=[Depends(requerir_roles("ADM"))]
)


@router.get("/cli", status_code=status.HTTP_200_OK)
def obtener_usuarios_cli(db: Session = Depends(get_db)):
    """Obtiene todos los usuarios del lado de clientes"""
    try:
        service = UsuariosCLIService(db)
        response = service.get_usuarios_cli()

        rows = response.get("rows", [])
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron usuarios del lado de clientes",
            )

        return {
            "message": "Usuarios del lado de clientes obtenidos exitosamente",
            "data": rows,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/cli", status_code=status.HTTP_201_CREATED)
def crear_nuevo_usuario_cli(
    usuario_data: UsuarioCliCreate, db: Session = Depends(get_db)
):
    """Crea un nuevo usuario del lado de clientes"""
    try:
        service = UsuariosCLIService(db)
        response = service.crear_usuario_cli(usuario_data.model_dump())

        rows = response.get("rows", [])
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo crear el usuario cliente",
            )

        db.commit()
        return {
            "message": "Usuario cliente creado exitosamente",
            "data": rows[0],
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.patch("/cli/{usuario_id}/datos", status_code=status.HTTP_200_OK)
def actualizar_datos_usuario_cli(
    usuario_id: int,
    usuario_data: UsuarioCliUpdateDatos,
    db: Session = Depends(get_db),
):
    """Actualiza datos personales de un usuario cliente"""
    try:
        service = UsuariosCLIService(db)
        response = service.actualizar_usuario_cli(
            usuario_id, usuario_data.model_dump()
        )

        rows = response.get("rows", [])
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo actualizar el usuario cliente",
            )

        return {
            "message": "Datos del usuario cliente actualizados exitosamente",
            "data": rows,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.patch("/cli/{usuario_id}/rol", status_code=status.HTTP_200_OK)
def actualizar_rol_usuario_cli(
    usuario_id: int,
    usuario_data: UsuarioCliUpdateRol,
    db: Session = Depends(get_db),
):
    """Actualiza el rol de un usuario cliente"""
    try:
        service = UsuariosCLIService(db)
        response = service.actualizar_rol_usuario_cli(
            usuario_id, usuario_data.rol_id
        )

        rows = response.get("rows", [])
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo actualizar el rol del usuario cliente",
            )

        return {
            "message": "Rol del usuario cliente actualizado exitosamente",
            "data": rows,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.patch("/cli/{usuario_id}/estado", status_code=status.HTTP_200_OK)
def cambiar_estado_usuario_cli(
    usuario_id: int, activo: bool, db: Session = Depends(get_db)
):
    """Activa o desactiva un usuario cliente"""
    try:
        service = UsuariosCLIService(db)
        response = service.cambiar_estado_usuario_cli(usuario_id, activo)

        rows = response.get("rows", [])
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo actualizar el estado del usuario cliente",
            )

        return {
            "message": "Estado del usuario cliente actualizado exitosamente",
            "data": rows,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )