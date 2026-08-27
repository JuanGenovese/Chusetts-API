from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

from src.domains.compras.routes import router as compras_router
from src.domains.gestion.routes import router as gestion_router
from src.domains.usuarios.routes import router as usuarios_router
from src.domains.ventas.routes import router as ventas_router



app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "project": settings.PROJECT_NAME, "version": settings.PROJECT_VERSION}


# Register domain routers under /api
app.include_router(compras_router, prefix=settings.API_V1_STR)
app.include_router(gestion_router, prefix=settings.API_V1_STR)
app.include_router(usuarios_router, prefix=settings.API_V1_STR)
app.include_router(ventas_router, prefix=settings.API_V1_STR)
