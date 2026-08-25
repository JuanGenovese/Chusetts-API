from fastapi import APIRouter

router = APIRouter(prefix="/ventas", tags=["Ventas"])


@router.get("/tickets")
def list_tickets():
    """List sales tickets."""
    return {"message": "Ventas domain scaffold ready"}
