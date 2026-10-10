"""
Servicio de Predicciones — RF02
Orquesta la validación, llamada a Gemini y persistencia de predicciones.
"""
from dataclasses import dataclass

from app.integrations.gemini_client import (
    GeminiNoDisponibleError,
    RespuestaGeminiInvalidaError,
    generar_pronostico,
)
from app.repositories.historicos_repo import (
    MCPNoDisponibleError,
    ProductoNoEncontradoError,
    obtener_historicos,
)
from app.repositories.predicciones_repo import insertar_o_actualizar_prediccion

MINIMO_HISTORICOS = 4  # RF02-CA1


class DatosInsuficientesError(Exception):
    """El producto no tiene el mínimo de registros históricos requeridos."""


@dataclass
class ResultadoPrediccion:
    nombre_producto:  str
    periodo:          str
    cantidad_estimada: int
    fue_actualizado:  bool  # True si sobrescribió un registro anterior (RF02-CA6)


def generar_prediccion(producto_id: int, periodo: str) -> ResultadoPrediccion:
    """
    1. Obtiene históricos vía MCP.
    2. Verifica que existan al menos 4 registros de periodos distintos.
    3. Invoca la API de Gemini.
    4. Persiste el resultado.
    5. Retorna el resultado con indicación de si fue actualización.

    Propagaciones:
    - ProductoNoEncontradoError  → el producto no existe
    - MCPNoDisponibleError       → Servidor MCP no responde
    - DatosInsuficientesError    → menos de 4 históricos
    - GeminiNoDisponibleError    → API Gemini no disponible
    - RespuestaGeminiInvalidaError → respuesta no parseable
    """
    historicos = obtener_historicos(producto_id)  # puede lanzar ProductoNoEncontradoError o MCPNoDisponibleError

    # Verificar mínimo de datos (RF02-CA1)
    periodos_distintos = {h.periodo for h in historicos}
    if len(periodos_distintos) < MINIMO_HISTORICOS:
        raise DatosInsuficientesError(
            f"El producto tiene {len(periodos_distintos)} periodo(s) con datos históricos. "
            f"Se requieren al menos {MINIMO_HISTORICOS} periodos distintos para generar una predicción."
        )

    nombre_producto = historicos[0].nombre_producto

    # Generar pronóstico con Gemini (RF02-CA2)
    cantidad_estimada = generar_pronostico(nombre_producto, periodo, historicos)

    # Persistir y retornar (RF02-CA6)
    fue_actualizado = insertar_o_actualizar_prediccion(producto_id, periodo, cantidad_estimada)

    return ResultadoPrediccion(
        nombre_producto=nombre_producto,
        periodo=periodo,
        cantidad_estimada=cantidad_estimada,
        fue_actualizado=fue_actualizado,
    )
