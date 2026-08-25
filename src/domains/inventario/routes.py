from fastapi import APIRouter

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.get("/productos")
def list_products():
    """List products and stock availability."""
    return {"message": "Inventario domain scaffold ready"}
