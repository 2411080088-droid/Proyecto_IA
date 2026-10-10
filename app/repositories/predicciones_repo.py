"""
Repositorio de Predicciones — RF02, RF03
Accede directamente a SQLite para insertar y consultar predicciones.
"""
import sqlite3
from dataclasses import dataclass
from typing import List, Optional

from app.config import settings


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


@dataclass
class Prediccion:
    id_producto:      int
    nombre_producto:  str
    periodo:          str   # formato AAAA-WNN
    demanda_estimada: int   # >= 0
    fecha_generacion: str


def insertar_o_actualizar_prediccion(
    producto_id: int,
    periodo: str,
    cantidad_estimada: int,
) -> bool:
    """
    Inserta o actualiza (INSERT OR REPLACE) la predicción en SQLite.
    Retorna True si sobrescribió un registro existente, False si fue inserción nueva.
    """
    conn = _get_conn()
    try:
        cur = conn.cursor()
        # Verificar si ya existe para poder notificar al planificador (RF02-CA6)
        cur.execute(
            "SELECT id_prediccion FROM prediccion WHERE id_producto = ? AND periodo = ?",
            (producto_id, periodo),
        )
        existia = cur.fetchone() is not None

        cur.execute(
            """
            INSERT INTO prediccion (id_producto, periodo, demanda_estimada)
            VALUES (?, ?, ?)
            ON CONFLICT(id_producto, periodo) DO UPDATE SET
                demanda_estimada  = excluded.demanda_estimada,
                fecha_generacion  = datetime('now')
            """,
            (producto_id, periodo, cantidad_estimada),
        )
        conn.commit()
        return existia
    finally:
        conn.close()


def obtener_predicciones() -> List[Prediccion]:
    """Retorna todas las predicciones ordenadas por periodo ASC."""
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT pr.id_producto, p.nombre AS nombre_producto,
                   pr.periodo, pr.demanda_estimada, pr.fecha_generacion
            FROM prediccion pr
            JOIN producto p ON p.id_producto = pr.id_producto
            ORDER BY pr.periodo ASC
            """
        )
        return [
            Prediccion(
                id_producto=row["id_producto"],
                nombre_producto=row["nombre_producto"],
                periodo=row["periodo"],
                demanda_estimada=row["demanda_estimada"],
                fecha_generacion=row["fecha_generacion"],
            )
            for row in cur.fetchall()
        ]
    finally:
        conn.close()


def obtener_prediccion(producto_id: int, periodo: str) -> Optional[Prediccion]:
    """Retorna una predicción específica o None si no existe."""
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT pr.id_producto, p.nombre AS nombre_producto,
                   pr.periodo, pr.demanda_estimada, pr.fecha_generacion
            FROM prediccion pr
            JOIN producto p ON p.id_producto = pr.id_producto
            WHERE pr.id_producto = ? AND pr.periodo = ?
            """,
            (producto_id, periodo),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return Prediccion(
            id_producto=row["id_producto"],
            nombre_producto=row["nombre_producto"],
            periodo=row["periodo"],
            demanda_estimada=row["demanda_estimada"],
            fecha_generacion=row["fecha_generacion"],
        )
    finally:
        conn.close()
