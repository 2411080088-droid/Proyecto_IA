"""
Router de Históricos — RF01
Expone GET /historicos y delega la lógica al Servicio de Históricos.
"""
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.repositories.historicos_repo import MCPNoDisponibleError, ProductoNoEncontradoError
from app.services.historicos_service import consultar_historicos

router = APIRouter(prefix="/historicos", tags=["Históricos"])


@router.get("", summary="Consultar datos históricos de un producto")
def get_historicos(
    producto_id: int = Query(..., description="Identificador del producto"),
) -> JSONResponse:
    """
    Retorna los datos históricos de demanda para el producto indicado.

    - HTTP 200 + lista si hay registros.
    - HTTP 200 + mensaje informativo si el producto existe pero no tiene históricos.
    - HTTP 404 si el producto no existe en la base de datos.
    - HTTP 503 + opción de reintento si el Servidor MCP no responde en 5 s.
    """
    try:
        historicos = consultar_historicos(producto_id)
    except ProductoNoEncontradoError as exc:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Producto no encontrado",
                "detalle": str(exc),
            },
        )
    except MCPNoDisponibleError as exc:
        return JSONResponse(
            status_code=503,
            content={
                "error": "Servidor de datos no disponible",
                "detalle": str(exc),
                "reintento": "Vuelva a realizar la consulta en unos segundos.",
            },
        )

    if not historicos:
        return JSONResponse(
            status_code=200,
            content={
                "mensaje": f"No existen registros históricos disponibles para el producto con id={producto_id}.",
                "producto_id": producto_id,
                "historicos": [],
            },
        )

    return JSONResponse(
        status_code=200,
        content={
            "producto_id":     producto_id,
            "nombre_producto": historicos[0].nombre_producto,
            "total_registros": len(historicos),
            "historicos": [
                {
                    "periodo":         h.periodo,
                    "nombre_producto": h.nombre_producto,
                    "demanda_real":    h.demanda_real,
                }
                for h in historicos
            ],
        },
    )
