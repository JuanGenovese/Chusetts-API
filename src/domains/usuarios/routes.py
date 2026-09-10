from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.core.dependencies import requerir_roles
from src.domains.usuarios.schemas import (
    UsuarioAdmCreate,
    UsuarioAdmUpdateDatos,
    UsuarioAdmUpdateRol,
)
from src.domains.usuarios.services import UsuariosService

router = APIRouter(
    prefix="/usuarios", 
    tags=["Usuarios"],
    dependencies=[Depends(requerir_roles("ADM"))]
)

@router.get("/", status_code=status.HTTP_200_OK)
def obtener_usuarios(
    db: Session = Depends(get_db)
):
    """Obtiene todos los usuarios administrativos"""
    try:
        service = UsuariosService(db)
        response = service.get_usuarios()

        rows = response.get("rows", [])
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron usuarios administrativos"
            )

        return {
            "message": "Usuarios administrativos obtenidos exitosamente",
            "data": rows
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_nuevo_usuario(
    usuario_data: UsuarioAdmCreate,
    db: Session = Depends(get_db)
):
    """Crea un nuevo usuario del lado administrativo"""
    try:
        service = UsuariosService(db)
        response = service.crear_usuario(usuario_data.model_dump())

        rows = response.get("rows", [])
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo crear el usuario"
            )
            
        db.commit()
        return {
            "message": "Usuario administrativo creado exitosamente",
            "data": rows[0]
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{usuario_id}/datos", status_code=status.HTTP_200_OK)
def actualizar_datos_usuario(
    usuario_id: int,
    usuario_data: UsuarioAdmUpdateDatos,
    db: Session = Depends(get_db)
):
    """Actualiza nombre, apellido y/o DNI de un usuario administrativo"""
    try:
        service = UsuariosService(db)
        response = service.actualizar_usuario(usuario_id, usuario_data.model_dump())

        rows = response.get("rows", [])
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo actualizar el usuario"
            )

        return {
            "message": "Datos del usuario actualizados exitosamente",
            "data": rows
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{usuario_id}/rol", status_code=status.HTTP_200_OK)
def actualizar_rol_usuario(
    usuario_id: int,
    usuario_data: UsuarioAdmUpdateRol,
    db: Session = Depends(get_db)
):
    """Actualiza el rol de un usuario administrativo"""
    try:
        service = UsuariosService(db)   
        response = service.actualizar_rol_usuario(usuario_id, usuario_data.rol_id)

        rows = response.get("rows", [])
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo actualizar el rol del usuario"
            )

        return {
            "message": "Rol del usuario actualizado exitosamente",
            "data": rows
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{usuario_id}/estado", status_code=status.HTTP_200_OK)
def cambiar_estado_usuario(
    usuario_id: int,
    activo: bool,
    db: Session = Depends(get_db)
):
    """Activa o desactiva un usuario administrativo"""
    try:
        service = UsuariosService(db)
        response = service.cambiar_estado_usuario(usuario_id, activo)

        rows = response.get("rows", [])
        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo actualizar el estado del usuario"
            )

        return {
            "message": "Estado del usuario actualizado exitosamente",
            "data": rows
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )