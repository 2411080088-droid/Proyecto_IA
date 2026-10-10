"""
Router de Predicciones — RF02, RF03
POST /predicciones  → genera y persiste una nueva predicción
GET  /predicciones  → lista todas las predicciones generadas
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator

from app.integrations.gemini_client import GeminiNoDisponibleError, RespuestaGeminiInvalidaError
from app.repositories.historicos_repo import MCPNoDisponibleError, ProductoNoEncontradoError
from app.repositories.predicciones_repo import obtener_predicciones
from app.services.predicciones_service import DatosInsuficientesError, generar_prediccion

router = APIRouter(prefix="/predicciones", tags=["Predicciones"])


class SolicitudPrediccion(BaseModel):
    producto_id: int
    periodo: str  # formato AAAA-WNN, ej. "2024-W11"

    @field_validator("periodo")
    @classmethod
    def validar_formato_periodo(cls, v: str) -> str:
        import re
        if not re.match(r"^\d{4}-W\d{2}$", v):
            raise ValueError("El periodo debe estar en formato AAAA-WNN, por ejemplo '2024-W11'.")
        return v


@router.post("", summary="Generar predicción de demanda para un producto y periodo")
def post_prediccion(solicitud: SolicitudPrediccion) -> JSONResponse:
    """
    Genera y persiste una predicción de demanda.

    - HTTP 201  → predicción creada por primera vez.
    - HTTP 200  → predicción actualizada (registro anterior sobrescrito).
    - HTTP 422  → datos históricos insuficientes (< 4 periodos).
    - HTTP 404  → producto no encontrado.
    - HTTP 503  → Servidor MCP o API Gemini no disponibles.
    """
    try:
        resultado = generar_prediccion(solicitud.producto_id, solicitud.periodo)
    except ProductoNoEncontradoError as exc:
        return JSONResponse(status_code=404, content={"error": "Producto no encontrado", "detalle": str(exc)})
    except DatosInsuficientesError as exc:
        return JSONResponse(
            status_code=422,
            content={"error": "Datos históricos insuficientes", "detalle": str(exc)},
        )
    except (MCPNoDisponibleError,) as exc:
        return JSONResponse(
            status_code=503,
            content={
                "error": "Servidor de datos no disponible",
                "detalle": str(exc),
                "reintento": "Vuelva a intentarlo en unos segundos.",
            },
        )
    except (GeminiNoDisponibleError, RespuestaGeminiInvalidaError) as exc:
        return JSONResponse(
            status_code=503,
            content={"error": "Servicio de predicción no disponible", "detalle": str(exc)},
        )

    status_code = 200 if resultado.fue_actualizado else 201
    content = {
        "nombre_producto":  resultado.nombre_producto,
        "periodo":          resultado.periodo,
        "cantidad_estimada": resultado.cantidad_estimada,
        "actualizado":      resultado.fue_actualizado,
    }
    if resultado.fue_actualizado:
        content["mensaje"] = "La predicción anterior fue actualizada con el nuevo valor."

    return JSONResponse(status_code=status_code, content=content)


@router.get("", summary="Listar todas las predicciones generadas")
def get_predicciones() -> JSONResponse:
    """
    Retorna la lista de predicciones ordenadas por periodo ASC en formato AAAA-WNN.
    HTTP 200 + lista, o HTTP 200 + mensaje informativo si no hay predicciones.
    """
    predicciones = obtener_predicciones()

    if not predicciones:
        return JSONResponse(
            status_code=200,
            content={"mensaje": "Aún no se han generado predicciones.", "predicciones": []},
        )

    return JSONResponse(
        status_code=200,
        content={
            "total": len(predicciones),
            "predicciones": [
                {
                    "nombre_producto":  p.nombre_producto,
                    "periodo":          p.periodo,
                    "cantidad_estimada": p.demanda_estimada,
                    "fecha_generacion": p.fecha_generacion,
                }
                for p in predicciones
            ],
        },
    )
