"""
Router de Métricas — RF05
GET /metricas → calcula y retorna MAE y MAPE del modelo
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.metricas_service import SinDatosComparablesError, calcular_metricas

router = APIRouter(prefix="/metricas", tags=["Métricas"])


@router.get("", summary="Calcular métricas de evaluación del modelo (MAE y MAPE)")
def get_metricas() -> JSONResponse:
    """
    Calcula MAE y MAPE usando los pares (prediccion, dato_historico) disponibles.

    - HTTP 200  → métricas con 4 decimales y unidades.
    - HTTP 200  → mensaje informativo si no hay datos comparables.
    """
    try:
        resultado = calcular_metricas()
    except SinDatosComparablesError as exc:
        return JSONResponse(
            status_code=200,
            content={
                "mensaje": str(exc),
                "mae":  None,
                "mape": None,
            },
        )

    content = {
        "mae": {
            "valor":  resultado.mae,
            "unidad": "unidades de demanda",
        },
        "mape": {
            "valor":  resultado.mape,
            "unidad": "%",
        },
        "pares_utilizados":    resultado.pares_utilizados,
        "pares_excluidos_mape": resultado.pares_excluidos_mape,
    }
    if resultado.pares_excluidos_mape > 0:
        content["nota_mape"] = (
            f"Se excluyeron {resultado.pares_excluidos_mape} par(es) del cálculo del MAPE "
            "porque el dato histórico era igual a cero."
        )

    return JSONResponse(status_code=200, content=content)
