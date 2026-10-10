"""
Repositorio de Históricos — RF01, RF06
Consulta los datos históricos exclusivamente a través del Servidor MCP (solo lectura).
Usa httpx con timeout de 5 segundos según RF01-CA5 y RF01-CA6.
"""
from dataclasses import dataclass
from typing import List

import httpx

from app.config import settings


class MCPNoDisponibleError(Exception):
    """El Servidor MCP no respondió en el plazo máximo de 5 segundos."""


class ProductoNoEncontradoError(Exception):
    """El producto solicitado no existe en la base de datos."""


@dataclass
class DatoHistorico:
    periodo:         str   # formato AAAA-WNN
    nombre_producto: str
    demanda_real:    int   # >= 0


def obtener_historicos(producto_id: int) -> List[DatoHistorico]:
    """
    Llama a GET /historicos?producto_id=... del Servidor MCP.
    Retorna la lista de DatoHistorico ordenada por periodo ASC.
    Lanza MCPNoDisponibleError si el MCP no responde en 5 s.
    Lanza ProductoNoEncontradoError si el producto no existe (HTTP 404).
    """
    url = f"{settings.MCP_BASE_URL}/historicos"
    try:
        response = httpx.get(url, params={"producto_id": producto_id}, timeout=5.0)
    except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError) as exc:
        raise MCPNoDisponibleError(
            "El Servidor MCP no está disponible. Verifique que esté en ejecución e intente nuevamente."
        ) from exc

    if response.status_code == 404:
        raise ProductoNoEncontradoError(
            f"No se encontró el producto con id={producto_id} en la base de datos."
        )

    if response.status_code != 200:
        raise MCPNoDisponibleError(
            f"El Servidor MCP retornó un error inesperado (HTTP {response.status_code})."
        )

    data = response.json()
    historicos = [
        DatoHistorico(
            periodo=item["periodo"],
            nombre_producto=item["nombre_producto"],
            demanda_real=int(item["demanda_real"]),
        )
        for item in data.get("historicos", [])
    ]
    # Garantizar orden ascendente por periodo (Propiedad 3 de requirements.md)
    historicos.sort(key=lambda h: h.periodo)
    return historicos
