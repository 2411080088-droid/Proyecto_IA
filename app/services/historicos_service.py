"""
Servicio de Históricos — RF01
Orquesta la consulta de datos históricos a través del Repositorio de Históricos.
"""
from typing import List

from app.repositories.historicos_repo import (
    DatoHistorico,
    MCPNoDisponibleError,
    ProductoNoEncontradoError,
    obtener_historicos,
)


def consultar_historicos(producto_id: int) -> List[DatoHistorico]:
    """
    Retorna la lista de datos históricos para el producto, ordenada por periodo ASC.
    Propaga MCPNoDisponibleError y ProductoNoEncontradoError al router.
    """
    return obtener_historicos(producto_id)
