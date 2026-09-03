from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.dependencies import verificar_autenticacion_global

from src.domains.auth.routes import router as auth_router
from src.domains.compras.routes import router as compras_router
from src.domains.gestion.routes import router as gestion_router
from src.domains.usuarios.adm.routes import router as usuarios_adm_router
from src.domains.usuarios.cli.routes import router as usuarios_cli_router
from src.domains.ventas.routes import router as ventas_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    dependencies=[Depends(verificar_autenticacion_global)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME, "version": settings.PROJECT_VERSION}


app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(compras_router, prefix=settings.API_V1_STR)
app.include_router(gestion_router, prefix=settings.API_V1_STR)
app.include_router(usuarios_adm_router, prefix=settings.API_V1_STR)
app.include_router(usuarios_cli_router, prefix=settings.API_V1_STR )
app.include_router(ventas_router, prefix=settings.API_V1_STR)

