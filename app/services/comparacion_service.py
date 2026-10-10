"""
Servicio de Comparación — RF04
Combina predicción y dato histórico del mismo producto y periodo,
y calcula la diferencia absoluta.
"""
from dataclasses import dataclass
from typing import Optional

from app.repositories.comparacion_repo import (
    obtener_prediccion_para_comparacion,
    verificar_producto_existe,
)
from app.repositories.historicos_repo import (
    MCPNoDisponibleError,
    obtener_historicos,
)


class ProductoNoExisteError(Exception):
    """El producto no existe en la base de datos."""


@dataclass
class ResultadoComparacion:
    nombre_producto:    str
    periodo:            str
    prediccion:         Optional[int]
    dato_historico:     Optional[int]
    diferencia_absoluta: Optional[int]
    mensaje:            Optional[str]   # informativo cuando falta uno de los valores


def comparar(producto_id: int, periodo: str) -> ResultadoComparacion:
    """
    Obtiene la predicción desde SQLite y el dato histórico vía MCP.
    Calcula la diferencia absoluta solo cuando ambos existen.

    Lanza ProductoNoExisteError si el producto no está en la BD.
    Propaga MCPNoDisponibleError si el MCP no responde.
    """
    if not verificar_producto_existe(producto_id):
        raise ProductoNoExisteError(
            f"No se encontró el producto con id={producto_id} en la base de datos."
        )

    prediccion = obtener_prediccion_para_comparacion(producto_id, periodo)

    # Obtener dato histórico vía MCP
    historicos = obtener_historicos(producto_id)  # puede lanzar MCPNoDisponibleError
    historico_para_periodo = next(
        (h for h in historicos if h.periodo == periodo), None
    )

    nombre_producto = (
        prediccion.nombre_producto
        if prediccion
        else (historicos[0].nombre_producto if historicos else f"Producto {producto_id}")
    )

    if prediccion and historico_para_periodo:
        diferencia = abs(prediccion.demanda_estimada - historico_para_periodo.demanda_real)
        return ResultadoComparacion(
            nombre_producto=nombre_producto,
            periodo=periodo,
            prediccion=prediccion.demanda_estimada,
            dato_historico=historico_para_periodo.demanda_real,
            diferencia_absoluta=diferencia,
            mensaje=None,
        )

    if prediccion and not historico_para_periodo:
        return ResultadoComparacion(
            nombre_producto=nombre_producto,
            periodo=periodo,
            prediccion=prediccion.demanda_estimada,
            dato_historico=None,
            diferencia_absoluta=None,
            mensaje=f"No existe un dato histórico para el periodo {periodo}. Solo se muestra la predicción.",
        )

    if not prediccion and historico_para_periodo:
        return ResultadoComparacion(
            nombre_producto=nombre_producto,
            periodo=periodo,
            prediccion=None,
            dato_historico=historico_para_periodo.demanda_real,
            diferencia_absoluta=None,
            mensaje=f"No existe una predicción para el periodo {periodo}. Solo se muestra el dato histórico.",
        )

    # Ninguno existe
    return ResultadoComparacion(
        nombre_producto=nombre_producto,
        periodo=periodo,
        prediccion=None,
        dato_historico=None,
        diferencia_absoluta=None,
        mensaje=f"No existe ni predicción ni dato histórico para el periodo {periodo}.",
    )
