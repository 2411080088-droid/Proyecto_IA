"""
Router de Productos — soporte para el frontend
GET /productos → lista productos activos consultando SQLite directamente.
No pasa por el Servidor MCP porque listar productos no es un dato histórico (RF01)
ni una predicción; es metadata de catálogo que el frontend necesita para poblar
los selectores. Traza a RF01, RF02, RF04 (todos requieren seleccionar un producto).
"""
import sqlite3

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.config import settings

router = APIRouter(prefix="/productos", tags=["Productos"])


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


@router.get("", summary="Listar todos los productos disponibles")
def get_productos() -> JSONResponse:
    """
    Retorna la lista de productos activos con id, nombre, unidad de medida y categoría.
    HTTP 200 siempre (lista vacía si no hay productos activos).
    """
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                p.id_producto,
                p.nombre,
                p.unidad_medida,
                c.nombre AS categoria
            FROM producto p
            JOIN categoria_producto c ON c.id_categoria = p.id_categoria
            WHERE p.activo = 1
            ORDER BY p.nombre ASC
            """
        )
        productos = [
            {
                "id_producto":   row["id_producto"],
                "nombre":        row["nombre"],
                "unidad_medida": row["unidad_medida"],
                "categoria":     row["categoria"],
            }
            for row in cur.fetchall()
        ]
        return JSONResponse(status_code=200, content={"productos": productos})
    finally:
        conn.close()
