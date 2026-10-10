"""
Backend principal — FastAPI
Sistema de predicción de demanda de productos frescos y ultrafrescos
Supermercados Peruanos S.A.

El módulo de configuración valida GEMINI_API_KEY al importarse;
si no está definida el proceso termina con mensaje de error (RNF02).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# La importación de settings valida las variables de entorno al arranque (RNF02)
from app.config import settings  # noqa: F401

from app.routers import (
    historicos_router,
    predicciones_router,
    comparacion_router,
    metricas_router,
    productos_router,
)

app = FastAPI(
    title="API de Predicción de Demanda — Supermercados Peruanos S.A.",
    description=(
        "Prototipo de predicción de demanda de productos frescos y ultrafrescos. "
        "Consulta históricos (RF01), genera predicciones (RF02), visualiza resultados (RF03), "
        "compara pronóstico con real (RF04) y calcula métricas MAE/MAPE (RF05)."
    ),
    version="1.0.0",
)

# CORS permisivo para desarrollo local (frontend HTML/JS en el mismo equipo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de routers
app.include_router(historicos_router.router)
app.include_router(predicciones_router.router)
app.include_router(comparacion_router.router)
app.include_router(metricas_router.router)
app.include_router(productos_router.router)


@app.get("/", tags=["Estado"])
def raiz():
    return {"estado": "ok", "mensaje": "API de predicción de demanda en línea."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
