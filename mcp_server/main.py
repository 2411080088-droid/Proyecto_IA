"""
Servidor MCP — RF06
Servidor FastAPI independiente que opera en modo exclusivo de solo lectura.
- Solo acepta peticiones HTTP GET.
- Rechaza POST, PUT, PATCH y DELETE con HTTP 405.
- No ejecuta ningún INSERT, UPDATE ni DELETE contra la base de datos.
Puerto por defecto: 8001
"""
import os
import sqlite3
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Query, Request, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH: str = os.getenv("DATABASE_PATH", "database/prediccion_demanda.db")

app = FastAPI(
    title="Servidor MCP — Solo Lectura",
    description="Exposición de datos históricos en modo exclusivo de solo lectura (RF06).",
    version="1.0.0",
)


def get_connection() -> sqlite3.Connection:
    """Abre una conexión SQLite en modo solo lectura."""
    db_path = Path(DATABASE_PATH)
    if not db_path.exists():
        raise FileNotFoundError(f"Base de datos no encontrada: {db_path.resolve()}")
    conn = sqlite3.connect(f"file:{db_path.resolve()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


# ── Middleware: bloquear métodos de escritura ─────────────────────────────────
@app.middleware("http")
async def rechazar_escrituras(request: Request, call_next):
    """Rechaza cualquier método que no sea GET con HTTP 405."""
    if request.method.upper() != "GET":
        return JSONResponse(
            status_code=405,
            content={
                "error": "Método no permitido",
                "detalle": (
                    f"El Servidor MCP opera en modo exclusivo de solo lectura. "
                    f"El método '{request.method}' no está permitido. "
                    "Use HTTP GET para consultar datos."
                ),
            },
            headers={"Allow": "GET"},
        )
    return await call_next(request)


# ── Endpoints ─────────────────────────────────────────────────────────────────
@app.get("/historicos", summary="Consultar datos históricos de un producto")
def get_historicos(
    producto_id: int = Query(..., description="Identificador del producto a consultar"),
) -> JSONResponse:
    """
    Retorna los datos históricos de demanda para el producto indicado.
    Si el producto no existe retorna HTTP 404.
    Si no hay históricos para el producto retorna lista vacía con HTTP 200.
    Ordena por periodo de forma ascendente.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()

        # Verificar que el producto existe
        cur.execute("SELECT id_producto, nombre FROM producto WHERE id_producto = ?", (producto_id,))
        producto = cur.fetchone()
        if producto is None:
            return JSONResponse(
                status_code=404,
                content={
                    "error": "Producto no encontrado",
                    "detalle": f"No existe un producto con id_producto={producto_id} en la base de datos.",
                },
            )

        # Consultar históricos — solo SELECT, nunca INSERT/UPDATE/DELETE
        cur.execute(
            """
            SELECT
                dh.periodo,
                p.nombre   AS nombre_producto,
                dh.demanda_real
            FROM dato_historico dh
            JOIN producto p ON p.id_producto = dh.id_producto
            WHERE dh.id_producto = ?
            ORDER BY dh.periodo ASC
            """,
            (producto_id,),
        )
        rows = cur.fetchall()

        historicos = [
            {
                "periodo":          row["periodo"],
                "nombre_producto":  row["nombre_producto"],
                "demanda_real":     row["demanda_real"],
            }
            for row in rows
        ]

        return JSONResponse(
            status_code=200,
            content={
                "producto_id":      producto_id,
                "nombre_producto":  producto["nombre"],
                "historicos":       historicos,
            },
        )
    finally:
        conn.close()


@app.get("/productos", summary="Listar todos los productos disponibles")
def get_productos() -> JSONResponse:
    """Retorna la lista de todos los productos activos."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT p.id_producto, p.nombre, p.unidad_medida, c.nombre AS categoria
            FROM producto p
            JOIN categoria_producto c ON c.id_categoria = p.id_categoria
            WHERE p.activo = 1
            ORDER BY p.nombre ASC
            """
        )
        rows = cur.fetchall()
        productos = [
            {
                "id_producto":   row["id_producto"],
                "nombre":        row["nombre"],
                "unidad_medida": row["unidad_medida"],
                "categoria":     row["categoria"],
            }
            for row in rows
        ]
        return JSONResponse(status_code=200, content={"productos": productos})
    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mcp_server.main:app", host="0.0.0.0", port=8001, reload=False)
