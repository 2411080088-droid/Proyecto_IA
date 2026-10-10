"""
Router de Comparación — RF04
GET /comparacion → compara demanda pronosticada con demanda real
"""
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.repositories.historicos_repo import MCPNoDisponibleError
from app.services.comparacion_service import ProductoNoExisteError, comparar

router = APIRouter(prefix="/comparacion", tags=["Comparación"])


@router.get("", summary="Comparar predicción con dato histórico real")
def get_comparacion(
    producto_id: int  = Query(..., description="Identificador del producto"),
    periodo: str      = Query(..., description="Periodo en formato AAAA-WNN, ej. 2024-W05"),
) -> JSONResponse:
    """
    Compara la predicción y el dato histórico para el mismo producto y periodo.

    - HTTP 200  → comparación completa con diferencia absoluta, o parcial con mensaje.
    - HTTP 404  → producto no encontrado.
    - HTTP 503  → Servidor MCP no disponible.
    """
    try:
        resultado = comparar(producto_id, periodo)
    except ProductoNoExisteError as exc:
        return JSONResponse(
            status_code=404,
            content={"error": "Producto no encontrado", "detalle": str(exc)},
        )
    except MCPNoDisponibleError as exc:
        return JSONResponse(
            status_code=503,
            content={
                "error": "Servidor de datos no disponible",
                "detalle": str(exc),
                "reintento": "Vuelva a intentarlo en unos segundos.",
            },
        )

    content = {
        "nombre_producto":    resultado.nombre_producto,
        "periodo":            resultado.periodo,
        "prediccion":         resultado.prediccion,
        "dato_historico":     resultado.dato_historico,
        "diferencia_absoluta": resultado.diferencia_absoluta,
    }
    if resultado.mensaje:
        content["mensaje"] = resultado.mensaje

    return JSONResponse(status_code=200, content=content)
