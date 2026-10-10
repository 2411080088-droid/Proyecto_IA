"""
Repositorio de Comparación — RF04
Consulta predicciones en SQLite y verifica existencia de productos.
El dato histórico se obtiene desde el Repositorio de Históricos vía MCP.
"""
import sqlite3
from typing import Optional

from app.config import settings
from app.repositories.predicciones_repo import Prediccion, obtener_prediccion


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def obtener_prediccion_para_comparacion(
    producto_id: int, periodo: str
) -> Optional[Prediccion]:
    """Retorna la predicción almacenada para el producto y periodo, o None."""
    return obtener_prediccion(producto_id, periodo)


def verificar_producto_existe(producto_id: int) -> bool:
    """Retorna True si el producto existe en la base de datos."""
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id_producto FROM producto WHERE id_producto = ?", (producto_id,)
        )
        return cur.fetchone() is not None
    finally:
        conn.close()
